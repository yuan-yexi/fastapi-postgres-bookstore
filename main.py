import databases
import sqlalchemy
from fastapi import FastAPI, Request

DATABASE_URL = "postgresql://postgres:password@localhost:5432/store"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer),
    sqlalchemy.Column("publisher_id", sqlalchemy.ForeignKey("publisher._id"), index=True),
)

readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("first_name", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("last_name", sqlalchemy.String, primary_key=True),
    sqlalchemy.UniqueConstraint("id", name="unique_id")
)


publisher = sqlalchemy.Table(
    "publisher",
    metadata,
    sqlalchemy.Column("_id", sqlalchemy.Integer, primary_key=True, index=True, unique=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)

# engine = sqlalchemy.create_engine(DATABASE_URL)
# metadata.create_all(engine)  # create all tables

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/books/")
async def get_all_books():
    query = books.select()
    return await database.fetch_all(query)


@app.post("/books/")
async def create_book(request: Request):
    data = await request.json()
    query = books.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}


@app.post("/readers/")
async def create_book(request: Request):
    data = await request.json()
    query = readers.insert().values(**data)
    last_record_id = await database.execute(query)
    return {"id": last_record_id}
