import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.database import Base, Profile, Clip, PlaylistEntity, Playlist, UserProfile, ProfileClip, ProfilePlaylist

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_suno_db_models.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_module():
    """Create all tables before running tests"""
    Base.metadata.create_all(bind=engine)

def teardown_module():
    """Drop all tables after running tests"""
    Base.metadata.drop_all(bind=engine)

def test_suno_profile_model():
    """Test Profile model creation"""
    db = TestingSessionLocal()
    try:
        profile = Profile(
            external_user_id="test_user_123",
            display_name="Test User",
            handle="testuser",
            profile_description="A test profile",
            avatar_image_url="https://example.com/avatar.jpg",
            is_verified=False,
            stats={"followers_count": 10, "clips_count": 5}
        )
        
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        # Verify the profile was created with correct attributes
        assert profile.handle == "testuser"
        assert profile.display_name == "Test User"
        assert profile.external_user_id == "test_user_123"
        assert profile.is_verified is False
        
    finally:
        db.close()

def test_suno_clip_model():
    """Test Clip model creation"""
    db = TestingSessionLocal()
    try:
        clip = Clip(
            clip_id="test_clip_123",
            title="Test Clip Title",
            status="complete",
            play_count=10,
            upvote_count=5,
            user_id="test_user_123",
            display_name="Test User",
            handle="testuser",
            video_url="https://example.com/video.mp4",
            audio_url="https://example.com/audio.mp3",
            image_url="https://example.com/image.jpg",
            major_model_version="v4",
            model_name="chirp-v4",
            metadata_info={"prompt": "Test prompt", "tags": "test, music"},
            is_public=True,
            is_explicit=False
        )
        
        db.add(clip)
        db.commit()
        db.refresh(clip)
        
        # Verify the clip was created with correct attributes
        assert clip.clip_id == "test_clip_123"
        assert clip.title == "Test Clip Title"
        assert clip.status == "complete"
        assert clip.play_count == 10
        assert clip.is_public is True
        
    finally:
        db.close()

def test_suno_playlist_entity_model():
    """Test PlaylistEntity model creation"""
    db = TestingSessionLocal()
    try:
        playlist = PlaylistEntity(
            playlist_id="test_playlist_123",
            name="Test Playlist",
            description="A test playlist description",
            image_url="https://example.com/playlist.jpg",
            num_total_results=10,
            current_page=1,
            is_owned=True,
            is_public=True,
            is_hidden=False,
            user_display_name="Test User",
            user_handle="testuser",
            upvote_count=5,
            play_count=100,
            song_count=5
        )
        
        db.add(playlist)
        db.commit()
        db.refresh(playlist)
        
        # Verify the playlist was created with correct attributes
        assert playlist.playlist_id == "test_playlist_123"
        assert playlist.name == "Test Playlist"
        assert playlist.num_total_results == 10
        assert playlist.is_owned is True
        assert playlist.is_public is True
        
    finally:
        db.close()

def test_suno_playlist_clip_model():
    """Test Playlist model creation (association model)"""
    db = TestingSessionLocal()
    try:
        # Create a playlist and clip first
        playlist = PlaylistEntity(
            playlist_id="test_playlist_assoc",
            name="Test Association Playlist",
            description="A test playlist for associations"
        )
        clip = Clip(
            clip_id="test_clip_assoc",
            title="Test Association Clip",
            status="complete",
            user_id="test_user_123",
            display_name="Test User",
            handle="testuser"
        )
        
        db.add(playlist)
        db.add(clip)
        db.commit()
        
        # Refresh to get the IDs
        db.refresh(playlist)
        db.refresh(clip)
        
        # Create the association
        playlist_clip = Playlist(
            playlist_id=playlist.id,
            clip_id=clip.id,
            relative_index=1
        )
        
        db.add(playlist_clip)
        db.commit()
        db.refresh(playlist_clip)
        
        # Verify the association was created
        assert playlist_clip.playlist_id == playlist.id
        assert playlist_clip.clip_id == clip.id
        assert playlist_clip.relative_index == 1
        
    finally:
        db.close()

def test_user_suno_profile_model():
    """Test UserProfile model creation (association model)"""
    db = TestingSessionLocal()
    try:
        # Create a profile first
        profile = Profile(
            external_user_id="test_user_assoc",
            display_name="Test Assoc User",
            handle="testuserassoc",
            profile_description="A test profile for associations"
        )
        
        db.add(profile)
        db.commit()
        db.refresh(profile)
        
        # Create the association (using a test UUID for user_id)
        user_profile = UserProfile(
            user_id="123e4567-e89b-12d3-a456-426614174000",  # Test UUID
            profile_id=profile.id
        )
        
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
        
        # Verify the association was created
        assert str(user_profile.profile_id) == str(profile.id)
        assert str(user_profile.user_id) == "123e4567-e89b-12d3-a456-42614174000"
        
    finally:
        db.close()

def test_profile_clip_model():
    """Test ProfileClip model creation (association model)"""
    db = TestingSessionLocal()
    try:
        # Create a profile and clip first
        profile = Profile(
            external_user_id="test_profile_clip",
            display_name="Test Profile Clip",
            handle="testprofileclip",
            profile_description="A test profile for clip associations"
        )
        clip = Clip(
            clip_id="test_clip_profile",
            title="Test Clip for Profile",
            status="complete",
            user_id="test_profile_clip",
            display_name="Test Profile Clip",
            handle="testprofileclip"
        )
        
        db.add(profile)
        db.add(clip)
        db.commit()
        
        # Refresh to get the IDs
        db.refresh(profile)
        db.refresh(clip)
        
        # Create the association
        profile_clip = ProfileClip(
            profile_id=profile.id,
            clip_id=clip.id
        )
        
        db.add(profile_clip)
        db.commit()
        db.refresh(profile_clip)
        
        # Verify the association was created
        assert profile_clip.profile_id == profile.id
        assert profile_clip.clip_id == clip.id
        
    finally:
        db.close()

def test_profile_playlist_model():
    """Test ProfilePlaylist model creation (association model)"""
    db = TestingSessionLocal()
    try:
        # Create a profile and playlist first
        profile = Profile(
            external_user_id="test_profile_playlist",
            display_name="Test Profile Playlist",
            handle="testprofileplaylist",
            profile_description="A test profile for playlist associations"
        )
        playlist = PlaylistEntity(
            playlist_id="test_playlist_profile",
            name="Test Playlist for Profile",
            description="A test playlist for profile associations"
        )
        
        db.add(profile)
        db.add(playlist)
        db.commit()
        
        # Refresh to get the IDs
        db.refresh(profile)
        db.refresh(playlist)
        
        # Create the association
        profile_playlist = ProfilePlaylist(
            profile_id=profile.id,
            playlist_id=playlist.id
        )
        
        db.add(profile_playlist)
        db.commit()
        db.refresh(profile_playlist)
        
        # Verify the association was created
        assert profile_playlist.profile_id == profile.id
        assert profile_playlist.playlist_id == playlist.id
        
    finally:
        db.close()

if __name__ == "__main__":
    setup_module()
    try:
        test_suno_profile_model()
        test_suno_clip_model()
        test_suno_playlist_entity_model()
        test_suno_playlist_clip_model()
        test_user_suno_profile_model()
        test_profile_clip_model()
        test_profile_playlist_model()
        print("All database model tests passed!")
    finally:
        teardown_module()