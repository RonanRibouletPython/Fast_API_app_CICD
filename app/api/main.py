from fastapi import FastAPI
from app.routes import activity, user, partner_request
from app.db.db_setup import engine_postgres, Base
from app.db.models.user import User
from app.db.models.partner_request import PartnerRequest
from app.db.models.activity import Activity

# commented because the database is created with alembic
Base.metadata.create_all(bind=engine_postgres)

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
app.include_router(partner_request.router)



