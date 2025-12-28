import logging
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from database.session import engine
from models.database import Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
