from sqlalchemy import create_engine
from app.core.config import config

creds_postgres = {
    "username": config["creds_postgres"]["username"],
    "password": config["creds_postgres"]["password"],
    "port": config["creds_postgres"]["port"],
    "host": config["creds_postgres"]["host"],
    "db": config["creds_postgres"]["db"],
}


conn_str = f"postgresql+psycopg2://{creds_postgres['username']}:{creds_postgres['password']}@{creds_postgres['host']}:{creds_postgres['port']}/{creds_postgres['db']}"
engine_postgres = create_engine(conn_str)

