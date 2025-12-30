from pydantic import BaseModel, ConfigDict
from typing import Optional, Union
from datetime import datetime

class MetadataDTO(BaseModel):
    tags: Optional[str] = None
    prompt: Optional[str] = None
    duration: Optional[str] = None

class ClipBaseDTO(BaseModel):
    id: str
    title: str
    audio_url: Optional[str]
    image_url: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ClipSlimDTO(BaseModel):
    id: str
    title: str
    audio_url: Optional[str]
    video_url: Optional[str]
    image_url: Optional[str]
    metadata: Optional[MetadataDTO]
    model_config = ConfigDict(from_attributes=True)


class ClipDTO(BaseModel):
    id: str
    title: str
    video_url: Optional[str]
    audio_url: Optional[str]
    image_url: Optional[str]
    image_large_url: Optional[str]
    clip_metadata: Optional[MetadataDTO]
    caption: Optional[str]
    type: Optional[str]
    duration: Optional[Union[float, str]]
    task: Optional[str]
    user_id: Optional[str]
    display_name: Optional[str]
    handle: Optional[str]
    user_avatar_image_url: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class PlaylistClipDTO(BaseModel):
    id: str
    title: str
    audio_url: Optional[str]
    video_url: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    image_large_url: Optional[str] = None
    clip_metadata: Optional[MetadataDTO] = None
    caption: Optional[str] = None
    type: Optional[str] = None
    stream: Optional[bool] = None
    make_instrumental: Optional[bool] = None
    task: Optional[str] = None
    can_remix: Optional[bool] = None
    is_remix: Optional[bool] = None
    priority: Optional[int] = None
    has_stem: Optional[bool] = None
    video_is_stale: Optional[bool] = None
    uses_latest_model: Optional[bool] = None
    is_liked: Optional[bool] = False
    user_id: Optional[str] = None
    display_name: Optional[str] = None
    handle: Optional[str] = None
    is_handle_updated: Optional[bool] = None
    avatar_image_url: Optional[str] = None
    is_trashed: Optional[bool] = None
    is_public: Optional[bool] = None
    is_following_creator: Optional[bool] = None
    explicit: Optional[bool] = None
    comment_count: Optional[int] = None
    flag_count: Optional[int] = None
    is_contest_clip: Optional[bool] = None
    has_hook: Optional[bool] = None
    model_config = ConfigDict(from_attributes=True)
