from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import config
from app.utils.logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

env = os.getenv("ENV", "local")

if env == "local":
    creds_postgres = {
        "username": config["creds_postgres_local"]["username"],
        "password": config["creds_postgres_local"]["password"],
        "port": config["creds_postgres_local"]["port"], 
        "host": config["creds_postgres_local"]["host"],
        "db": config["creds_postgres_local"]["db"],
    }
    
if env == "docker":
    creds_postgres = {
        "username": config["creds_postgres_docker"]["username"],
        "password": config["creds_postgres_docker"]["password"],
        "port": config["creds_postgres_docker"]["port"],
        "host": config["creds_postgres_docker"]["host"],
        "db": config["creds_postgres_docker"]["db"],
    }


conn_str = f"postgresql+psycopg2://{creds_postgres['username']}:{creds_postgres['password']}@{creds_postgres['host']}:{creds_postgres['port']}/{creds_postgres['db']}"
engine_postgres = create_engine(
    conn_str, future=True, connect_args={"options": "-csearch_path=app_schema"}
    )

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_postgres, future=True)



