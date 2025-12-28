from sqlalchemy.orm import Session
from typing import Optional
from backend.models.database import Playlist, Clip
from backend.models.dtos import PlaylistCreate, PlaylistResponse
import requests
from datetime import datetime
import json


def get_playlist_by_id(db: Session, playlist_id: str) -> Optional[PlaylistResponse]:
    """Get a playlist by its ID from the database"""
    playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()
    if playlist:
        return PlaylistResponse.model_validate(playlist)
    return None


def create_or_update_playlist(db: Session, playlist_data: dict) -> PlaylistResponse:
    """Create or update a playlist in the database"""
    playlist_id = playlist_data.get("id", "")
    name = playlist_data.get("name", "Unknown Playlist")
    description = playlist_data.get("description", "")
    data = playlist_data  # This is now a dict that will be stored in the JSON column

    # Check if playlist already exists
    existing_playlist = db.query(Playlist).filter(Playlist.playlist_id == playlist_id).first()

    if existing_playlist:
        # Update existing playlist
        existing_playlist.name = name
        existing_playlist.description = description
        existing_playlist.data = data if data else {}
        # last_synced will be automatically updated by SQLAlchemy due to onupdate=func.now()
        db.commit()
        db.refresh(existing_playlist)
        return PlaylistResponse.model_validate(existing_playlist)
    else:
        # Create new playlist
        db_playlist = Playlist(
            playlist_id=playlist_id,
            name=name,
            description=description,
            data=data
        )
        db.add(db_playlist)
        db.commit()
        db.refresh(db_playlist)
        return PlaylistResponse.model_validate(db_playlist)


def fetch_suno_playlist(playlist_id: str) -> dict:
    """Fetch playlist data from Suno API"""
    url = f"https://studio-api.prod.suno.com/api/playlist/{playlist_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract the playlist information from the response
        # The API response contains the playlist data at the root level
        # The clips are in the 'playlist_clips' field, each containing a 'clip' object
        playlist_clips = data.get("playlist_clips", [])
        # Extract just the clip objects from each playlist clip entry
        clips = []
        for playlist_clip in playlist_clips:
            if "clip" in playlist_clip:
                clips.append(playlist_clip["clip"])
        
        playlist_info = {
            "id": data.get("id", playlist_id),
            "name": data.get("name", ""),
            "description": data.get("description", ""),
            "clips": clips,  # Extracted clip objects
            "image_url": data.get("image_url"),
            "user_display_name": data.get("user_display_name"),
            "user_handle": data.get("user_handle"),
            "user_avatar_image_url": data.get("user_avatar_image_url"),
            "upvote_count": data.get("upvote_count", 0),
            "play_count": data.get("play_count", 0),
            "song_count": data.get("song_count", 0),
            "created_at": data.get("created_at"),
            "is_public": data.get("is_public", False),
        }
        
        return playlist_info
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch playlist from Suno API: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Failed to decode JSON response from Suno API")


def sync_playlist_with_suno(db: Session, playlist_id: str) -> PlaylistResponse:
    """Fetch playlist from Suno API and save to database"""
    playlist_data = fetch_suno_playlist(playlist_id)
    return create_or_update_playlist(db, playlist_data)


def fetch_all_user_playlists(user_handle: str, sort_by: str = "upvote_count") -> dict:
    raise Exception("Failed to decode JSON response from Suno API")


def get_all_user_playlists(db: Session, user_handle: str, sort_by: str = "upvote_count") -> list[PlaylistResponse]:
    """Get all playlists for a user, either from database or by fetching from Suno API"""
    # First, try to fetch from the API
    playlists_data = fetch_all_user_playlists(user_handle, sort_by)
    
    # Create or update each playlist in the database
    playlist_responses = []
    for playlist_data in playlists_data["playlists"]:
        playlist_response = create_or_update_playlist(db, playlist_data)
        playlist_responses.append(playlist_response)
    
    return playlist_responses
