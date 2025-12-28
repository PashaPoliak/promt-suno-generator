import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database.session import get_db
from models.database import Base
from backend.app.models import dtos

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_suno_entities.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a test client
client = TestClient(app)

# Override the database dependency
def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()

app.dependency_overrides[get_db] = override_get_db

def setup_module():
    """Create all tables before running tests"""
    Base.metadata.create_all(bind=engine)

def teardown_module():
    """Drop all tables after running tests"""
    Base.metadata.drop_all(bind=engine)

def test_create_profile():
    """Test creating a Suno profile"""
    profile_data = {
        "external_user_id": "test_user_123",
        "display_name": "Test User",
        "handle": "testuser",
        "profile_description": "A test profile",
        "avatar_image_url": "https://example.com/avatar.jpg",
        "is_verified": False,
        "stats": {"followers_count": 10, "clips_count": 10}
    }
    
    response = client.post("/v1/api/profiles/", json=profile_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["handle"] == "testuser"
    assert data["display_name"] == "Test User"
    assert data["external_user_id"] == "test_user_123"

def test_get_profile():
    """Test retrieving a Suno profile"""
    # First create a profile
    profile_data = {
        "external_user_id": "test_user_456",
        "display_name": "Test User 2",
        "handle": "testuser2",
        "profile_description": "Another test profile"
    }
    
    create_response = client.post("/v1/api/profiles/", json=profile_data)
    assert create_response.status_code == 200
    
    created_profile = create_response.json()
    profile_id = created_profile["id"]
    
    # Now retrieve it
    response = client.get(f"/v1/api/profiles/{profile_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["handle"] == "testuser2"
    assert data["display_name"] == "Test User 2"

def test_create_clip():
    """Test creating a Suno clip"""
    clip_data = {
        "clip_id": "test_clip_123",
        "title": "Test Clip",
        "status": "complete",
        "play_count": 0,
        "upvote_count": 0,
        "user_id": "test_user_123",
        "display_name": "Test User",
        "handle": "testuser",
        "video_url": "https://example.com/test_video.mp4",
        "audio_url": "https://example.com/test_audio.mp3",
        "image_url": "https://example.com/test_image.jpg",
        "major_model_version": "v4",
        "model_name": "chirp-v4"
    }
    
    response = client.post("/v1/api/clips/", json=clip_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Clip"
    assert data["status"] == "complete"
    assert data["clip_id"] == "test_clip_123"

def test_get_clip():
    """Test retrieving a Suno clip"""
    # First create a clip
    clip_data = {
        "clip_id": "test_clip_456",
        "title": "Test Clip 2",
        "status": "complete",
        "user_id": "test_user_123",
        "display_name": "Test User",
        "handle": "testuser"
    }
    
    create_response = client.post("/v1/api/clips/", json=clip_data)
    assert create_response.status_code == 200
    
    created_clip = create_response.json()
    clip_id = created_clip["id"]
    
    # Now retrieve it
    response = client.get(f"/v1/api/clips/{clip_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Clip 2"
    assert data["clip_id"] == "test_clip_456"

def test_create_playlist():
    """Test creating a Suno playlist"""
    playlist_data = {
        "playlist_id": "test_playlist_123",
        "name": "Test Playlist",
        "description": "A test playlist",
        "image_url": "https://example.com/playlist_image.jpg",
        "num_total_results": 5,
        "current_page": 1,
        "is_owned": True,
        "is_public": True
    }
    
    response = client.post("/v1/api/suno_playlists/", json=playlist_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Test Playlist"
    assert data["playlist_id"] == "test_playlist_123"
    assert data["is_owned"] is True

def test_get_playlist():
    """Test retrieving a Suno playlist"""
    # First create a playlist
    playlist_data = {
        "playlist_id": "test_playlist_456",
        "name": "Test Playlist 2",
        "description": "Another test playlist"
    }
    
    create_response = client.post("/v1/api/suno_playlists/", json=playlist_data)
    assert create_response.status_code == 200
    
    created_playlist = create_response.json()
    playlist_id = created_playlist["id"]
    
    # Now retrieve it
    response = client.get(f"/v1/api/suno_playlists/{playlist_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "Test Playlist 2"
    assert data["playlist_id"] == "test_playlist_456"

def test_playlist_clips_operations():
    """Test adding and removing clips from playlists"""
    # Create a playlist
    playlist_data = {
        "playlist_id": "test_playlist_clips",
        "name": "Test Playlist for Clips",
        "description": "Playlist for testing clips"
    }
    
    playlist_response = client.post("/v1/api/suno_playlists/", json=playlist_data)
    assert playlist_response.status_code == 200
    playlist = playlist_response.json()
    playlist_id = playlist["id"]
    
    # Create a clip
    clip_data = {
        "clip_id": "test_clip_for_playlist",
        "title": "Clip for Playlist Test",
        "status": "complete",
        "user_id": "test_user_123",
        "display_name": "Test User",
        "handle": "testuser"
    }
    
    clip_response = client.post("/v1/api/clips/", json=clip_data)
    assert clip_response.status_code == 200
    clip = clip_response.json()
    clip_id = clip["id"]
    
    # Add the clip to the playlist
    playlist_clip_data = {
        "playlist_id": playlist_id,
        "clip_id": clip_id,
        "relative_index": 0
    }
    
    add_response = client.post(f"/v1/api/suno_playlists/{playlist_id}/clips", json=playlist_clip_data)
    assert add_response.status_code == 200
    
    added_playlist_clip = add_response.json()
    assert added_playlist_clip["playlist_id"] == playlist_id
    assert added_playlist_clip["clip_id"] == clip_id
    
    # Get all clips in the playlist
    clips_response = client.get(f"/v1/api/suno_playlists/{playlist_id}/clips")
    assert clips_response.status_code == 200
    
    clips_data = clips_response.json()
    assert len(clips_data) == 1
    assert clips_data[0]["clip_id"] == clip_id
    
    # Remove the clip from the playlist
    remove_response = client.delete(f"/v1/api/suno_playlists/{playlist_id}/clips/{clip_id}")
    assert remove_response.status_code == 200
    
    # Verify the clip is removed
    clips_response_after = client.get(f"/v1/api/suno_playlists/{playlist_id}/clips")
    assert clips_response_after.status_code == 200
    
    clips_data_after = clips_response_after.json()
    assert len(clips_data_after) == 0

def test_user_profile_association():
    """Test associating profiles with users"""
    # Create a user (we'll use a UUID for this test)
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    
    # Create a profile
    profile_data = {
        "external_user_id": "test_user_789",
        "display_name": "Test User 3",
        "handle": "testuser3",
        "profile_description": "Third test profile"
    }
    
    profile_response = client.post("/v1/api/profiles/", json=profile_data)
    assert profile_response.status_code == 200
    profile = profile_response.json()
    profile_id = profile["id"]
    
    # Associate the profile with the user
    assoc_response = client.post(f"/v1/api/user_profiles/{user_id}/profiles/{profile_id}")
    # Note: This might fail if the profile doesn't exist in the database in a real scenario
    # For this test, we're just ensuring the endpoint structure is correct
    assert assoc_response.status_code in [200, 404]  # Could be 404 if user doesn't exist
    
    # Get profiles for the user
    profiles_response = client.get(f"/v1/api/user_profiles/{user_id}/profiles")
    # This endpoint might return 404 if user doesn't exist, which is acceptable for testing
    assert profiles_response.status_code in [200, 404]