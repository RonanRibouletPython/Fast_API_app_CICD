from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
user = os.getenv("POSTGRE_USERNAME")
password = os.getenv("POSTGRE_PASSWORD")
port = os.getenv("POSTGRE_PORT")
host = os.getenv("POSTGRE_HOST")
dbname = os.getenv("POSTGRE_DB")

creds_postgres = {
    'host': host,
    'port': port,
    'user': user,
    'password': password,
    'dbname': dbname
}

conn_str = f"postgresql+psycopg2://{creds_postgres['user']}:{creds_postgres['password']}@{creds_postgres['host']}:{creds_postgres['port']}/{creds_postgres['dbname']}"
engine_postgres = create_engine(conn_str)

def test_connection():
    try:
        engine = create_engine(conn_str)
        engine.connect() 
        print("Connection successful!") 
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()

