from database import mongodb, MongoClip, MongoPlaylist, MongoProfile
from config.logging_config import get_logger

logger = get_logger(__name__)


class MongoClipDAO:
    def __init__(self):
        self.collection = mongodb.clips_collection

    async def create_clip(self, clip_data: dict):
        try:
            clip = MongoClip(**clip_data)
            clip_dict = clip.model_dump()
            # Remove id field if it's empty to let MongoDB generate ObjectId
            if 'id' in clip_dict and not clip_dict['id']:
                del clip_dict['id']
            result = await self.collection.insert_one(clip_dict)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating clip: {e}")
            raise

    async def get_clip_by_id(self, clip_id: str):
        try:
            clip = await self.collection.find_one({"id": clip_id})
            if clip:
                # Convert ObjectId to string if present
                if '_id' in clip and hasattr(clip['_id'], '__str__'):
                    if 'id' not in clip:  # Only set id if not already present
                        clip['id'] = str(clip['_id'])
                    del clip['_id']
                # Create and return a validated model instance, handling potential validation errors
                try:
                    validated_clip = MongoClip(**clip)
                    return validated_clip.model_dump()
                except Exception as validation_error:
                    logger.warning(f"Clip validation error for id {clip_id}: {validation_error}")
                    # Return the raw clip data if validation fails
                    return clip
            return clip
        except Exception as e:
            logger.error(f"Error getting clip by ID: {e}")
            raise

    async def get_all_clips(self, page: int = 0, size: int = 25):
        try:
            clips = []
            async for clip in self.collection.find().skip(page * size).limit(size):
                if clip:
                    # Convert ObjectId to string if present
                    if '_id' in clip and hasattr(clip['_id'], '__str__'):
                        if 'id' not in clip:  # Only set id if not already present
                            clip['id'] = str(clip['_id'])
                        del clip['_id']
                    # Create and append a validated model instance, handling potential validation errors
                    try:
                        validated_clip = MongoClip(**clip)
                        clips.append(validated_clip.model_dump())
                    except Exception as validation_error:
                        logger.warning(f"Clip validation error: {validation_error}")
                        # Append the raw clip data if validation fails
                        clips.append(clip)
                else:
                    clips.append(clip)
            return clips
        except Exception as e:
            logger.error(f"Error getting all clips: {e}")
            raise


class MongoPlaylistDAO:
    def __init__(self):
        self.collection = mongodb.playlists_collection

    async def create_playlist(self, playlist_data: dict):
        try:
            playlist = MongoPlaylist(**playlist_data)
            playlist_dict = playlist.model_dump()
            # Remove id field if it's empty to let MongoDB generate ObjectId
            if 'id' in playlist_dict and not playlist_dict['id']:
                del playlist_dict['id']
            result = await self.collection.insert_one(playlist_dict)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating playlist: {e}")
            raise

    async def get_playlist_by_id(self, playlist_id: str):
        try:
            playlist = await self.collection.find_one({"id": playlist_id})
            if playlist:
                # Convert ObjectId to string if present
                if '_id' in playlist and hasattr(playlist['_id'], '__str__'):
                    if 'id' not in playlist:  # Only set id if not already present
                        playlist['id'] = str(playlist['_id'])
                    del playlist['_id']
                # Create and return a validated model instance, handling potential validation errors
                try:
                    validated_playlist = MongoPlaylist(**playlist)
                    return validated_playlist.model_dump()
                except Exception as validation_error:
                    logger.warning(f"Playlist validation error for id {playlist_id}: {validation_error}")
                    # Return the raw playlist data if validation fails
                    return playlist
            return playlist
        except Exception as e:
            logger.error(f"Error getting playlist by ID: {e}")
            raise

    async def get_all_playlists(self, page: int = 0, size: int = 25):
        try:
            playlists = []
            async for playlist in self.collection.find().skip(page * size).limit(size):
                if playlist:
                    # Convert ObjectId to string if present
                    if '_id' in playlist and hasattr(playlist['_id'], '__str__'):
                        if 'id' not in playlist:  # Only set id if not already present
                            playlist['id'] = str(playlist['_id'])
                        del playlist['_id']
                    # Create and append a validated model instance, handling potential validation errors
                    try:
                        validated_playlist = MongoPlaylist(**playlist)
                        playlists.append(validated_playlist.model_dump())
                    except Exception as validation_error:
                        logger.warning(f"Playlist validation error: {validation_error}")
                        # Append the raw playlist data if validation fails
                        playlists.append(playlist)
                else:
                    playlists.append(playlist)
            return playlists
        except Exception as e:
            logger.error(f"Error getting all playlists: {e}")
            raise


class MongoProfileDAO:
    def __init__(self):
        self.collection = mongodb.profiles_collection

    async def create_profile(self, profile_data: dict):
        try:
            profile = MongoProfile(**profile_data)
            profile_dict = profile.model_dump()
            # Remove id field if it's empty to let MongoDB generate ObjectId
            if 'id' in profile_dict and not profile_dict['id']:
                del profile_dict['id']
            result = await self.collection.insert_one(profile_dict)
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            raise

    async def get_profile_by_handle(self, handle: str):
        try:
            profile = await self.collection.find_one({"handle": handle})
            
            # If profile doesn't exist or has empty clip_ids/playlist_ids, fetch from API and update/create it
            if not profile or not profile.get('clip_ids') or not profile.get('playlist_ids'):
                logger.info(f"Profile {handle} not found or missing clip/playlist IDs, fetching from API")
                from services.api import fetch_profile_from_suno
                api_data = fetch_profile_from_suno(handle)
                
                if api_data:
                    # Create or update profile with API data
                    profile_data = {
                        "handle": handle,
                        "display_name": api_data.get("display_name", ""),
                        "profile_description": api_data.get("bio", ""),
                        "avatar_image_url": api_data.get("avatar_url", ""),
                        "clip_ids": [clip["id"] for clip in api_data.get("clips", []) if clip.get("id")],
                        "playlist_ids": [playlist["id"] for playlist in api_data.get("playlists", []) if playlist.get("id")]
                    }
                    
                    # If profile exists, update it; otherwise, create it
                    if profile:
                        # Update existing profile
                        profile_id = profile.get('_id') or profile.get('id')
                        await self.collection.update_one(
                            {"_id": profile_id},
                            {"$set": profile_data}
                        )
                        # Fetch the updated profile
                        profile = await self.collection.find_one({"_id": profile_id})
                    else:
                        # Create new profile
                        profile_id = await self.create_profile(profile_data)
                        profile = await self.collection.find_one({"_id": profile_id})
            
            if profile:
                # Convert ObjectId to string if present
                if '_id' in profile and hasattr(profile['_id'], '__str__'):
                    if 'id' not in profile:  # Only set id if not already present
                        profile['id'] = str(profile['_id'])
                    del profile['_id']
                
                # Ensure all required fields exist with proper defaults
                if 'clip_ids' not in profile or profile['clip_ids'] is None:
                    profile['clip_ids'] = []
                if 'playlist_ids' not in profile or profile['playlist_ids'] is None:
                    profile['playlist_ids'] = []
                if 'handle' not in profile or profile['handle'] is None:
                    profile['handle'] = handle  # Use the handle from the parameter if not in the document
                if 'display_name' not in profile:
                    profile['display_name'] = profile.get('display_name', '')
                if 'profile_description' not in profile:
                    profile['profile_description'] = profile.get('profile_description', '')
                if 'avatar_image_url' not in profile:
                    profile['avatar_image_url'] = profile.get('avatar_image_url', '')
                
                # Create and return a validated model instance, handling potential validation errors
                try:
                    validated_profile = MongoProfile(**profile)
                    result = validated_profile.model_dump()
                    # Ensure clip_ids and playlist_ids are always present in the response with proper default values
                    result['clip_ids'] = result.get('clip_ids', [])
                    result['playlist_ids'] = result.get('playlist_ids', [])
                    return result
                except Exception as validation_error:
                    logger.warning(f"Profile validation error for handle {handle}: {validation_error}")
                    # Return the raw profile data if validation fails, ensuring arrays exist
                    profile['clip_ids'] = profile.get('clip_ids', [])
                    profile['playlist_ids'] = profile.get('playlist_ids', [])
                    return profile
            return profile
        except Exception as e:
            logger.error(f"Error getting profile by handle: {e}")
            raise

    async def get_all_profiles(self, page: int = 0, size: int = 25):
        try:
            profiles = []
            async for profile in self.collection.find().skip(page * size).limit(size):
                if profile:
                    # Convert ObjectId to string if present
                    if '_id' in profile and hasattr(profile['_id'], '__str__'):
                        if 'id' not in profile:  # Only set id if not already present
                            profile['id'] = str(profile['_id'])
                        del profile['_id']
                    
                    # Ensure all required fields exist with proper defaults
                    if 'clip_ids' not in profile or profile['clip_ids'] is None:
                        profile['clip_ids'] = []
                    if 'playlist_ids' not in profile or profile['playlist_ids'] is None:
                        profile['playlist_ids'] = []
                    if 'handle' not in profile:
                        profile['handle'] = profile.get('handle', '')
                    if 'display_name' not in profile:
                        profile['display_name'] = profile.get('display_name', '')
                    if 'profile_description' not in profile:
                        profile['profile_description'] = profile.get('profile_description', '')
                    if 'avatar_image_url' not in profile:
                        profile['avatar_image_url'] = profile.get('avatar_image_url', '')
                    
                    # Create and append a validated model instance, handling potential validation errors
                    try:
                        validated_profile = MongoProfile(**profile)
                        result = validated_profile.model_dump()
                        # Ensure clip_ids and playlist_ids are always present in the response with proper default values
                        result['clip_ids'] = result.get('clip_ids', [])
                        result['playlist_ids'] = result.get('playlist_ids', [])
                        profiles.append(result)
                    except Exception as validation_error:
                        logger.warning(f"Profile validation error: {validation_error}")
                        # Append the raw profile data if validation fails, ensuring arrays exist
                        profile['clip_ids'] = profile.get('clip_ids', [])
                        profile['playlist_ids'] = profile.get('playlist_ids', [])
                        profiles.append(profile)
                else:
                    profiles.append(profile)
            return profiles
        except Exception as e:
            logger.error(f"Error getting all profiles: {e}")
            raise