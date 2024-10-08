from app.db.db_setup import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()