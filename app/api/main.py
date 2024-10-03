from fastapi import FastAPI
from app.routes import activity, user
from app.db.db_setup import engine_postgres, Base

# commented because the database is created with alembic
# Base.metadata.create_all(bind=engine_postgres)

description = """
## Date Ideas

This is the API for couples to share date ideas and plan them.

"""

app = FastAPI(
    title="Date Ideas Application",
    description=description,
    summary="Application for my Cricri and I <3",
    version="0.0.1",
    contact={
        "name": "Riboulet Ronan",
        "email": "ronanriboulet@gmail.com",
    },
    )

app.include_router(activity.router)
app.include_router(user.router)



