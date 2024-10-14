from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import activity, user, partner_request
from app.db.db_setup import engine_postgres, Base
from fastapi.middleware.cors import CORSMiddleware

# Initialize the FastAPI app
app = FastAPI(
    title="Date Ideas Application",
    description="This is the API for couples to share date ideas and plan them.",
    version="0.0.1",
    contact={
        "name": "Riboulet Ronan",
        "email": "ronanriboulet@gmail.com",
    },
)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

# Uncomment if you're creating tables with Alembic; comment if using Alembic migrations
Base.metadata.create_all(bind=engine_postgres)

# Include routers
app.include_router(activity.router)
app.include_router(user.router)
app.include_router(partner_request.router)
