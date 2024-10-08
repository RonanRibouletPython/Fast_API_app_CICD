from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import config
from app.utils.logger import logger
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

Base = declarative_base()

env = os.getenv("ENV", "local")

def get_db_creds(env: str):
    if env == "local":
        return {
            "username": config["creds_postgres_local"]["username"],
            "password": config["creds_postgres_local"]["password"],
            "port": config["creds_postgres_local"]["port"], 
            "host": config["creds_postgres_local"]["host"],
            "db": config["creds_postgres_local"]["db"],
        }
    elif env == "docker":
        return {
            "username": config["creds_postgres_docker"]["username"],
            "password": config["creds_postgres_docker"]["password"],
            "port": config["creds_postgres_docker"]["port"],
            "host": config["creds_postgres_docker"]["host"],
            "db": config["creds_postgres_docker"]["db"],
        }
    else:
        raise ValueError(f"Unsupported environment: {env}")

creds_postgres = get_db_creds(env)


conn_str = f"postgresql+psycopg2://{quote_plus(creds_postgres['username'])}:{quote_plus(creds_postgres['password'])}@{creds_postgres['host']}:{creds_postgres['port']}/{creds_postgres['db']}"

engine_postgres = create_engine(
    conn_str,
    future=True,
    connect_args={"options": "-csearch_path=app_schema"},
    pool_size=10,  # Adjust based on your needs
    max_overflow=20,  # Number of connections to allow in overflow
)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine_postgres, 
    future=True
)

# Logging connection information
logger.info(f"Database connected at {creds_postgres['host']}:{creds_postgres['port']}")


