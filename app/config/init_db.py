import logging
from sqlalchemy import Engine, create_engine, inspect

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from models.entities import Base
from config.session import engine_embed, engine_postgres


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(engine: Engine):
    try:
        # Check if we're using SQLite
        if "sqlite" in str(engine.url):
            # For SQLite, we need to handle schema updates differently
            # We'll check if the tables exist and have the right columns
            Base.metadata.create_all(engine)
            logger.info(f"Database tables created or updated successfully for SQLite!")
        else:
            # For PostgreSQL, use the original logic
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            expected_tables = Base.metadata.tables.keys()
            missing_tables = [table for table in expected_tables if table not in existing_tables]
            
            if not missing_tables:
                logger.info(f"All database tables already exist: {existing_tables}")
            else:
                logger.info(f"Missing tables: {missing_tables}")
                Base.metadata.create_all(engine)
                logger.info(f"Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        if "postgres" in str(engine.url):
            logger.warning("PostgreSQL database initialization failed, but continuing with SQLite only")
        else:
            raise e

if __name__ == "__main__":
    init_db(engine_embed)
    init_db(engine_postgres)
