import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.core.config import config

creds_postgres = {
    "username": config["creds_postgres"]["username"],
    "password": config["creds_postgres"]["password"],
    "port": config["creds_postgres"]["port"],
    "host": config["creds_postgres"]["host"],
    "db": config["creds_postgres"]["db"],
}

@pytest.fixture
def db_engine():
    conn_str = f"postgresql+psycopg2://{creds_postgres['username']}:{creds_postgres['password']}@{creds_postgres['host']}:{creds_postgres['port']}/{creds_postgres['db']}"
    engine = create_engine(conn_str)
    yield engine
    engine.dispose()

def test_connection(db_engine):
    """
    Test if the connection to the PostgreSQL database is successful.
    """
    try:
        # Attempt to connect to the database
        with db_engine.connect() as conn:
            assert conn is not None
        print("Database connection successful!")
    except OperationalError as e:
        pytest.fail(f"Database connection failed: {e}")
        
def test_invalid_connection():
    """
    Test connection failure with incorrect credentials.
    """
    conn_str = "postgresql://wrong_user:wrong_password@localhost:5432/non_existent_db"
    engine = create_engine(conn_str)
    
    with pytest.raises(OperationalError):
        with engine.connect():
            pass