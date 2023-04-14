import databases
import sqlalchemy
from decouple import config
from fastapi import FastAPI, Request

DATABASE_URL = f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@localhost:5432/store"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("_id", sqlalchemy.Integer, primary_key=True, unique=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("author", sqlalchemy.String),
    sqlalchemy.Column("pages", sqlalchemy.Integer),
)

readers = sqlalchemy.Table(
    "readers",
    metadata,
    sqlalchemy.Column("_id", sqlalchemy.Integer, primary_key=True, index=True, unique=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
)

publisher = sqlalchemy.Table(
    "publisher",
    metadata,
    sqlalchemy.Column("_id", sqlalchemy.Integer, primary_key=True, index=True, unique=True),
)

readers_books = sqlalchemy.Table(
    "readers_books",
    metadata,
    sqlalchemy.Column("_id", sqlalchemy.Integer, primary_key=True, unique=True, index=True),
    sqlalchemy.Column("book_id", sqlalchemy.ForeignKey("books._id"), nullable=False),
    sqlalchemy.Column("reader_id", sqlalchemy.ForeignKey("readers._id"), nullable=False),
)


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
