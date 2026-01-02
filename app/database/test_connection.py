import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.postgres_connection import test_connection, engine
from database.postgres_models import Base

def create_tables():
    """Create all tables in the database"""
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    if test_connection():
        print("Successfully connected to the database")
        
        create_tables()
        print("Database setup completed successfully")
    else:
        print("Failed to connect to the database")