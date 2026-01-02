from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.settings import settings
import logging
import os

logger = logging.getLogger(__name__)

if settings.environment == "prod" or settings.environment == "dev":
    DATABASE_URL = settings.postgres_url
    engine = create_engine(DATABASE_URL)
else:
    os.makedirs("app", exist_ok=True)
    DATABASE_URL = "postgresql://admin:AFttyzTL6nzF7A4myOEFlFMazQ7dVefg@dpg-d5bf6otactks73ft9310-a.oregon-postgres.render.com/suno"
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False