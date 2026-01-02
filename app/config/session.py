from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from app.config.settings import settings
import os
import sys
import logging

logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    engine_postgres = create_engine(
        settings.postgres_url,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=300
    )
    with engine_postgres.connect() as conn:
        pass
    logger.info("PostgreSQL engine created successfully")
except Exception as e:
    logger.warning(f"Unexpected error creating PostgreSQL engine: {e}. Using dummy engine for fallback.")

os.makedirs("app", exist_ok=True)

engine_embed = create_engine(
    "sqlite:///app/suno.db",
    connect_args={"check_same_thread": False}
)

# Only create SessionPG if PostgreSQL engine is functional
try:
    if "memory" not in str(engine_postgres.url):
        SessionPG = sessionmaker(autocommit=False, autoflush=False, bind=engine_postgres)
    else:
        SessionPG = None
except:
    SessionPG = None

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_embed)


def get_db_pg():
    if SessionPG is None:
        # Return None or raise an exception to indicate PostgreSQL is unavailable
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="PostgreSQL service unavailable")
    db = SessionPG()
    try:
        yield db
    finally:
        db.close()


def get_db_sqlite():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

