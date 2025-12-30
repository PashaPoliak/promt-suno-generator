from datetime import datetime
from typing import Optional, Any

from models.profile import ProfileDTO
from models.clip import ClipSlimDTO, ClipDTO, MetadataDTO, ClipBaseDTO
from models.playlist import PlaylistDTO, PlaylistEntity
from models.entities import Profile, Clip, Playlist
from config.logging_config import get_logger

logger = get_logger(__name__)


def safe_str_convert(value: Any, default: str = "") -> str:
    try:
        return str(value)
    except (TypeError, ValueError):
        logger.warning(f"Failed to convert {value} to string, using default: {default}")
        return default


def safe_str_optional(value: Any, default: Optional[str] = None) -> Optional[str]:
    try:
        return str(value)
    except (TypeError, ValueError):
        logger.warning(f"Failed to convert {value} to string, using default: {default}")
        return default


def safe_int_convert(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        logger.warning(f"Failed to convert {value} to int, using default: {default}")
        return default


def safe_bool_convert(value: Any, default: bool = False) -> bool:
    try:
        return bool(value)
    except (TypeError, ValueError):
        logger.warning(f"Failed to convert {value} to bool, using default: {default}")
        return default


def safe_bool_optional(value: Any, default: Optional[bool] = None) -> Optional[bool]:
    try:
        return bool(value)
    except (TypeError, ValueError):
        logger.warning(f"Failed to convert {value} to bool, using default: {default}")
        return default


def safe_get_attr(obj: Any, attr: str, default: Any = None) -> Any:
    try:
        return getattr(obj, attr, default)
    except AttributeError:
        logger.warning(f"Attribute {attr} not found in object, using default: {default}")
        return default


def process_clip_metadata(metadata_dict: dict) -> dict:
    if not isinstance(metadata_dict, dict):
        return metadata_dict
    
    processed_metadata = metadata_dict.copy()
    
    if 'duration' in processed_metadata and processed_metadata['duration'] is not None:
        processed_metadata['duration'] = str(processed_metadata['duration'])
    
    return processed_metadata


def create_metadata_dto(metadata_dict: dict) -> MetadataDTO:
    duration_value = metadata_dict.get('duration')
    duration_str = str(duration_value) if duration_value is not None else None
    return MetadataDTO(
        tags=metadata_dict.get('tags'),
        prompt=metadata_dict.get('prompt'),
        duration=safe_str_optional(duration_str, None)
    )


def create_clips_dto_from_profile(profile: Profile):
    return [ClipSlimDTO(
        id=safe_str_convert(clip.id, ""),
        title=safe_str_convert(clip.title, ""),
        audio_url=safe_str_optional(clip.audio_url, None),
        video_url=safe_str_optional(clip.video_url, None),
        image_url=safe_str_optional(clip.image_url, None),
        metadata=create_metadata_dto(getattr(clip, 'clip_metadata', {}))
    ) for clip in profile.clips]


def create_clips_dto_from_playlist(clips):
    return [ClipSlimDTO(
        id=safe_str_convert(clip.id, ""),
        title=safe_str_convert(clip.title, ""),
        audio_url=safe_str_optional(clip.audio_url, None),
        video_url=safe_str_optional(clip.video_url, None),
        image_url=safe_str_optional(clip.image_url, None),
        metadata=create_metadata_dto(getattr(clip, 'clip_metadata', {}))
    ) for clip in clips]


def create_base_clips_dto(clips):
    return [
        ClipBaseDTO(
            id=safe_str_convert(clip.id, ""),
            title=safe_str_convert(clip.title, ""),
            audio_url=safe_str_optional(clip.audio_url, None),
            image_url=safe_str_optional(clip.image_url, None)
        ) for clip in clips
    ]


def create_playlist_dto(profile: Profile):
    return [to_playlist_dto(playlist, profile.clips) for playlist in profile.playlists]

def to_playlist(playlist: Playlist) -> PlaylistEntity:
    return PlaylistEntity(
        id=safe_str_convert(playlist.id, ""),
        name=safe_str_convert(playlist.name, ""),
        handle=safe_str_convert(getattr(playlist, 'user_handle', ''), ""),
        description=safe_str_optional(playlist.description, None),
        image_url=safe_str_optional(playlist.image_url, None),
        clips=create_clips_dto_from_playlist(playlist.clips)
    )

def to_playlist_dto(playlist: Playlist, clips) -> PlaylistDTO:
    return PlaylistDTO(
        id=safe_str_convert(playlist.id, ""),
        name=safe_str_convert(playlist.name, ""),
        handle=safe_str_convert(getattr(playlist.profile, 'handle', ''), "") if playlist.profile else "",
        description=safe_str_optional(playlist.description, None),
        image_url=safe_str_optional(playlist.image_url, None),
        clips=create_base_clips_dto(clips)
    )

def to_profile_dto(profile: Profile) -> ProfileDTO:
    return ProfileDTO(
        id=safe_str_convert(profile.id, ""),
        handle=safe_str_convert(profile.handle, ""),
        display_name=safe_str_convert(profile.display_name, ""),
        profile_description=safe_str_optional(profile.profile_description, None),
        avatar_image_url=safe_str_optional(profile.avatar_image_url, None),
        clips=create_clips_dto_from_profile(profile),
        playlists=create_playlist_dto(profile)
    )


def to_clip_dto(clip: Clip) -> ClipDTO:
    return ClipDTO(
        id=safe_str_convert(clip.id, ""),
        title=safe_str_convert(clip.title, ""),
        video_url=safe_get_attr(clip, 'video_url', None),
        audio_url=safe_get_attr(clip, 'audio_url', None),
        image_url=safe_get_attr(clip, 'image_url', None),
        image_large_url=safe_get_attr(clip, 'image_large_url', None),
        clip_metadata=create_metadata_dto(safe_get_attr(clip, 'clip_metadata', {})),
        caption=safe_get_attr(clip, 'caption', None),
        type=safe_get_attr(clip, 'type', None),
        duration=safe_get_attr(clip, 'duration', None),
        task=safe_get_attr(clip, 'task', None),
        user_id=safe_get_attr(clip, 'user_id', None),
        display_name=safe_get_attr(clip, 'display_name', None),
        handle=safe_get_attr(clip, 'handle', None),
        user_avatar_image_url=safe_get_attr(clip, 'avatar_image_url', None),
    )


def create_clip_slim(data: dict) -> Clip:
    return Clip(
        id=data["id"],
        status=data.get("status"),
        title=data.get("title"),
        play_count=data.get("play_count", 0),
        upvote_count=data.get("upvote_count", 0),
        allow_comments=data.get("allow_comments"),
        entity_type=data.get("entity_type"),
        video_url=data.get("video_url"),
        audio_url=data.get("audio_url"),
        image_url=data.get("image_url"),
        image_large_url=data.get("image_large_url"),
        major_model_version=data.get("major_model_version"),
        model_name=data.get("model_name"),
        clip_metadata=data.get("metadata"),
        caption=data.get("caption"),
        type=data.get("type"),
        duration=str(data.get("duration")) if data.get("duration") is not None else None,
        refund_credits=data.get("refund_credits"),
        stream=data.get("stream"),
        make_instrumental=data.get("make_instrumental"),
        can_remix=data.get("can_remix"),
        is_remix=data.get("is_remix"),
        priority=data.get("priority"),
        has_stem=data.get("has_stem"),
        video_is_stale=data.get("video_is_stale"),
        uses_latest_model=data.get("uses_latest_model"),
        is_liked=data.get("is_liked"),
        user_id=data.get("user_id"),
        display_name=data.get("display_name"),
        handle=data.get("handle"),
        is_handle_updated=data.get("is_handle_updated"),
        avatar_image_url=data.get("avatar_image_url"),
        is_trashed=data.get("is_trashed"),
        created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
        is_public=data.get("is_public"),
        explicit=data.get("explicit"),
        comment_count=data.get("comment_count"),
        flag_count=data.get("flag_count"),
        is_contest_clip=data.get("is_contest_clip"),
        has_hook=data.get("has_hook"),
        batch_index=data.get("batch_index"),
        is_pinned=data.get("is_pinned")
    )

