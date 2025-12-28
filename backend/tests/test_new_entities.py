import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.database import Base, Profile, Clip, PlaylistEntity, Playlist

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_new_entities.db"

test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def test_create_tables():
    """Test that all new entities can be created in the database"""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    
    # Verify tables exist by creating some test instances
    db: Session = TestingSessionLocal()
    
    try:
        # Test creating a Profile
        profile = Profile(
            external_user_id="test_user_123",
            display_name="Test User",
            handle="testuser",
            profile_description="A test profile",
            avatar_image_url="https://example.com/avatar.jpg"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        # Query the profile back to ensure it's properly loaded from the database
        retrieved_profile = db.query(Profile).filter(Profile.id == profile.id).first()
        assert retrieved_profile is not None
        assert retrieved_profile.handle == "testuser"
        assert retrieved_profile.display_name == "Test User"
        
        # Test creating a Clip
        clip = Clip(
            clip_id="test_clip_123",
            title="Test Clip",
            status="complete",
            play_count=0,
            upvote_count=0,
            user_id="test_user_123",
            display_name="Test User",
            handle="testuser"
        )
        db.add(clip)
        db.commit()
        db.refresh(clip)
        
        # Query the clip back to ensure it's properly loaded from the database
        retrieved_clip = db.query(Clip).filter(Clip.id == clip.id).first()
        assert retrieved_clip is not None
        assert retrieved_clip.title == "Test Clip"
        assert retrieved_clip.status == "complete"
        
        # Test creating a PlaylistEntity
        playlist = PlaylistEntity(
            playlist_id="test_playlist_123",
            name="Test Playlist",
            description="A test playlist"
        )
        db.add(playlist)
        db.commit()
        db.refresh(playlist)
        
        # Query the playlist back to ensure it's properly loaded from the database
        retrieved_playlist = db.query(PlaylistEntity).filter(PlaylistEntity.id == playlist.id).first()
        assert retrieved_playlist is not None
        assert retrieved_playlist.name == "Test Playlist"
        
        # Test creating a Playlist (association)
        playlist_clip = Playlist(
            playlist_id=playlist.id,
            clip_id=clip.id,
            relative_index=0
        )
        db.add(playlist_clip)
        db.commit()
        db.refresh(playlist_clip)
        
        # Query the association back to ensure it's properly loaded from the database
        retrieved_playlist_clip = db.query(Playlist).filter(Playlist.id == playlist_clip.id).first()
        assert retrieved_playlist_clip is not None
        assert str(retrieved_playlist_clip.playlist_id) == str(playlist.id)
        assert str(retrieved_playlist_clip.clip_id) == str(clip.id)
        
        print("All tests passed! New entities work correctly with the database.")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_create_tables()