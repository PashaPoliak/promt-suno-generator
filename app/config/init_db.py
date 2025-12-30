import logging
from sqlalchemy import create_engine

import sys
import os
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models.entities import Base
from config.settings import settings

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
        "sqlite:///app/suno.db",
        connect_args={"check_same_thread": False}
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info(f"Creating database tables...")
    Base.metadata.create_all(engine)
    logger.info(f"Database tables created successfully!")

if __name__ == "__main__":
    init_db()
