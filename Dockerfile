# Use the official PostgreSQL 12 image as the base image
FROM postgres:13

# Set the default environment variables
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB mydb

# Create a directory for the data volumes
RUN mkdir -p /var/lib/postgresql/data

# Set the ownership and permissions for the data directory
RUN chown -R postgres:postgres /var/lib/postgresql/data
RUN chmod 700 /var/lib/postgresql/data

# Set the data directory as a volume
VOLUME /var/lib/postgresql/data

# Expose the default PostgreSQL port
EXPOSE 5432

# Start the PostgreSQL server
CMD ["postgres"]
