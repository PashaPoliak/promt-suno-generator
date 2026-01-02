import logging
from sqlalchemy import create_engine, inspect

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models.entities import Base
from config.settings import settings

if settings.environment == "prod" or settings.environment == "dev":
    engine = create_engine(
        settings.postgres_url,
        pool_size=20,
        max_overflow=0,
        pool_pre_ping=True,
        pool_recycle=300
    )
else:
    # Ensure the app directory exists
    os.makedirs("app", exist_ok=True)
    engine = create_engine(
        "sqlite:///app/suno.db",
        connect_args={"check_same_thread": False}
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info(f"Checking if database tables exist...")
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    expected_tables = Base.metadata.tables.keys()
    missing_tables = [table for table in expected_tables if table not in existing_tables]
    
    if not missing_tables:
        logger.info(f"All database tables already exist: {existing_tables}")
    else:
        logger.info(f"Missing tables: {missing_tables}")
        logger.info(f"Creating missing database tables...")
        Base.metadata.create_all(engine)
        logger.info(f"Database tables created successfully!")

if __name__ == "__main__":
    init_db()
