from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base, Playlist
from config.settings import settings

def test_db_connection():
    """Test database connection and model creation"""
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if the Playlist table exists by trying to query it
        playlist_count = db.query(Playlist).count()
        print(f"Database connection successful!")
        print(f"Number of playlists in database: {playlist_count}")
        print(f"Playlist model is available and table exists")
        return True
    except Exception as e:
        print(f"Error accessing database: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection()