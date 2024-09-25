from sqlalchemy import Table, Column, Integer, String, MetaData
import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
from db_connection import engine_postgres

table_name = "test"

metadata = MetaData()

# Define the table structure
table = Table(
    table_name,
    metadata,
    Column("name", String(20)),
    Column("age", Integer),  # Changed to Integer for simplicity
)

test_data = [
    {"name": "John", "age": 20},
    {"name": "Jane", "age": 21},
]

# Check if the table already exists, and create it if not
with engine_postgres.connect() as conn:
    try:
        # Check if table exists
        if not engine_postgres.dialect.has_table(conn, table_name):
            table.create(engine_postgres)
            print(f"Table '{table_name}' created.")
        else:
            print(f"Table '{table_name}' already exists.")
        
        # Insert data (no need for explicit transaction management here)
        for row in test_data:
            conn.execute(table.insert().values(row)) 
        
        # Commit the transaction after the insert
        conn.commit()
        print(f"Inserted {len(test_data)} rows successfully.")
    
    except sa_exc.SQLAlchemyError as e:
        print(f"An error occurred: {e}")
