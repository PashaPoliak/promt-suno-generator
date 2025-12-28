import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.services.suno_playlist_service import get_all_user_playlists, fetch_all_user_playlists
from database.session import get_db
from models.database import Base

def test_get_all_playlists():
    """Test the get_all_playlists functionality"""
    print("Testing get all playlists functionality...")
    
    # Test fetching playlists from API
    try:
        print("\n1. Fetching all playlists from Suno API for user 'fotballpiraten'...")
        playlists_data = fetch_all_user_playlists("fotballpiraten", "upvote_count")
        print(f"Successfully fetched {playlists_data['total_playlists']} playlists")
        print(f"User stats: {playlists_data['user_stats']}")
        
        if playlists_data['playlists']:
            first_playlist = playlists_data['playlists'][0]
            print(f"First playlist: {first_playlist['name']} with {first_playlist['upvote_count']} upvotes")
        
    except Exception as e:
        print(f"Error fetching playlists from API: {e}")
        return
    
    # Test with database session
    try:
        print("\n2. Testing database integration...")
        DATABASE_URL = "sqlite:///./suno_prompts.db" # Using the same DB as the main app
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        
        # Create all tables
        from models.database import Base
        Base.metadata.create_all(bind=engine)
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        db = SessionLocal()
        
        try:
            playlists = get_all_user_playlists(db, "fotballpiraten", "upvote_count")
            print(f"Successfully stored/retrieved {len(playlists)} playlists in database")
            
            if playlists:
                first_playlist = playlists[0]
                print(f"First playlist from DB: {first_playlist.name} (ID: {first_playlist.playlist_id})")
                
        finally:
            db.close()
            
        print("\n3. Test completed successfully!")
        
    except Exception as e:
        print(f"Error during database test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_get_all_playlists()