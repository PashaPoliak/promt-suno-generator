from fastapi import APIRouter, HTTPException
from services.mongo_dao import MongoProfileDAO, MongoClipDAO, MongoPlaylistDAO
from config.logging_config import get_logger

logger = get_logger(__name__)

router = APIRouter()
profile_dao = MongoProfileDAO()
clip_dao = MongoClipDAO()
playlist_dao = MongoPlaylistDAO()


@router.get("")
async def get_profiles_v3():
    try:
        profiles = await profile_dao.get_all_profiles()
        return profiles
    except Exception as e:
        logger.error(f"Error retrieving profiles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{profile_handle}")
async def get_profile_by_handle_v3(profile_handle: str):
    try:
        # Get the raw profile data with IDs
        profile_data = await profile_dao.get_profile_by_handle(profile_handle)
        if not profile_data:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
        
        # Extract the clip and playlist IDs
        clip_ids = profile_data.get('clip_ids', [])
        playlist_ids = profile_data.get('playlist_ids', [])
        
        # Get clip objects by IDs
        clips = []
        for clip_id in clip_ids:
            try:
                clip_data = await clip_dao.get_clip_by_id(clip_id)
                if clip_data:
                    # Create a simplified clip object with the required fields
                    clip_obj = {
                        "id": clip_data.get('id', 'unknown'),
                        "title": clip_data.get('title', 'Unknown Title'),
                        "audio_url": clip_data.get('audio_url'),
                        "video_url": clip_data.get('video_url'),
                        "image_url": clip_data.get('image_url'),
                        "metadata": {
                            "tags": clip_data.get('clip_metadata', {}).get('tags'),
                            "prompt": clip_data.get('clip_metadata', {}).get('prompt'),
                            "duration": str(clip_data.get('duration')) if clip_data.get('duration') is not None else None
                        } if clip_data.get('clip_metadata') else None
                    }
                    clips.append(clip_obj)
            except Exception as clip_error:
                logger.error(f"Error processing clip {clip_id}: {clip_error}")
                continue  # Skip this clip if there's an error
        
        # Get playlist objects by IDs
        playlists = []
        for playlist_id in playlist_ids:
            try:
                playlist_data = await playlist_dao.get_playlist_by_id(playlist_id)
                if playlist_data:
                    # Create a simplified playlist object with the required fields
                    playlist_obj = {
                        "id": playlist_data.get('id', 'unknown'),
                        "name": playlist_data.get('name', 'Unknown Playlist'),
                        "handle": playlist_data.get('handle') or playlist_data.get('user_handle') or 'unknown',
                        "description": playlist_data.get('description', ''),
                        "image_url": playlist_data.get('image_url'),
                        "clips": []  # We'll populate this if needed
                    }
                    playlists.append(playlist_obj)
            except Exception as playlist_error:
                logger.error(f"Error processing playlist {playlist_id}: {playlist_error}")
                continue  # Skip this playlist if there's an error
        
        # Create and return a response with the desired structure
        response = {
            "id": profile_data.get('id'),
            "handle": profile_data.get('handle'),
            "display_name": profile_data.get('display_name', ''),
            "profile_description": profile_data.get('profile_description', ''),
            "avatar_image_url": profile_data.get('avatar_image_url', ''),
            "clips": clips,
            "playlists": playlists
        }
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving profile '{profile_handle}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")