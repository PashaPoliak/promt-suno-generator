from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

if settings.environment == "prod" or "dev" in settings.database_url:
    engine = create_engine(
        settings.postgres_url,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=300
    )
else:
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()