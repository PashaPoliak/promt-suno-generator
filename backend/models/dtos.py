from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class UserDTO(BaseModel):
    id: str
    handle: str
    display_name: str
    avatar_image_url: str

class PromptCreate(BaseModel):
    genre: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    instruments: Optional[str] = None
    voice_tags: Optional[str] = None
    lyrics_structure: Optional[str] = None
    custom_text: Optional[str] = None


class PromptResponse(BaseModel):
    id: UUID
    prompt_text: str
    parameters: Optional[dict] = None
    created_at: datetime
    generation_result: Optional[dict] = None

    class Config:
        from_attributes = True


class TemplateResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    instruments: Optional[str] = None
    voice_tags: Optional[str] = None
    lyrics_structure: Optional[str] = None
    created_at: datetime
    is_active: bool
    tags: List[str] = []

    class Config:
        from_attributes = True


class TemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    genre: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    instruments: Optional[str] = None
    voice_tags: Optional[str] = None
    lyrics_structure: Optional[str] = None
    is_active: bool = True


class GenerateRequest(BaseModel):
    genre: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    instruments: Optional[str] = None
    voice_tags: Optional[str] = None
    lyrics_structure: Optional[str] = None
    custom_elements: Optional[dict] = None


class GenerateResponse(BaseModel):
    id: UUID
    prompt_text: str
    generated_at: datetime
    parameters_used: dict
    validation_result: dict


class TagCreate(BaseModel):
    name: str
    description: Optional[str] = None
    tag_type: Optional[str] = None  # 'genre', 'mood', 'style', 'instrument', 'voice'


class TagResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    tag_type: Optional[str] = None  # 'genre', 'mood', 'style', 'instrument', 'voice'
    created_at: datetime

    class Config:
        from_attributes = True


class PlaylistCreate(BaseModel):
    playlist_id: str
    name: str
    description: Optional[str] = None
    data: Optional[dict] = None
    is_active: bool = True


class PlaylistResponse(BaseModel):
    id: UUID
    playlist_id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    last_synced: Optional[datetime] = None
    data: Optional[dict] = None
    
    class Config:
        from_attributes = True


class PlaylistListResponse(BaseModel):
    playlists: List[PlaylistResponse]
    total: int
    user_handle: str
    user_stats: Optional[dict] = None




class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Suno-related schemas
class ProfileCreate(BaseModel):
    external_user_id: str
    display_name: str
    handle: str
    profile_description: Optional[str] = None
    avatar_image_url: Optional[str] = None
    is_verified: Optional[bool] = False
    stats: Optional[dict] = None


class ProfileResponse(BaseModel):
    id: UUID
    external_user_id: str
    display_name: str
    handle: str
    profile_description: Optional[str] = None
    avatar_image_url: Optional[str] = None
    is_verified: bool
    stats: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class ProfileWithContentResponse(BaseModel):
    id: UUID
    external_user_id: str
    display_name: str
    handle: str
    profile_description: Optional[str] = None
    avatar_image_url: Optional[str] = None
    is_verified: bool
    stats: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    clips: List[ClipResponse] = []
    playlists: List[PlaylistEntity] = []

    class Config:
        from_attributes = True


class ClipCreate(BaseModel):
    clip_id: str
    title: str
    status: str = "complete"
    play_count: int = 0
    upvote_count: int = 0
    user_id: str
    display_name: str
    handle: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    image_large_url: Optional[str] = None
    major_model_version: Optional[str] = None
    model_name: Optional[str] = None
    metadata_info: Optional[dict] = None
    is_public: bool = True
    is_explicit: bool = False
    comment_count: int = 0
    is_trashed: bool = False
    is_liked: bool = False
    persona_id: Optional[str] = None
    data: Optional[dict] = None


class ClipResponse(BaseModel):
    id: UUID
    clip_id: str
    title: str
    status: str
    play_count: int
    upvote_count: int
    user_id: str
    display_name: str
    handle: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    image_large_url: Optional[str] = None
    major_model_version: Optional[str] = None
    model_name: Optional[str] = None
    metadata_info: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    is_public: bool
    is_explicit: bool
    comment_count: int
    is_trashed: bool
    is_liked: bool
    persona_id: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class PlaylistEntityCreate(BaseModel):
    playlist_id: str
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    num_total_results: int = 0
    current_page: int = 1
    is_owned: bool = False
    is_trashed: bool = False
    is_public: bool = True
    is_hidden: bool = False
    user_display_name: Optional[str] = None
    user_handle: Optional[str] = None
    user_avatar_image_url: Optional[str] = None
    upvote_count: int = 0
    dislike_count: int = 0
    flag_count: int = 0
    skip_count: int = 0
    play_count: int = 0
    song_count: int = 0
    is_discover_playlist: bool = False
    data: Optional[dict] = None


class PlaylistEntity(BaseModel):
    id: UUID
    playlist_id: str
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    num_total_results: int
    current_page: int
    is_owned: bool
    is_trashed: bool
    is_public: bool
    is_hidden: bool
    user_display_name: Optional[str] = None
    user_handle: Optional[str] = None
    user_avatar_image_url: Optional[str] = None
    upvote_count: int
    dislike_count: int
    flag_count: int
    skip_count: int
    play_count: int
    song_count: int
    is_discover_playlist: bool
    created_at: datetime
    updated_at: datetime
    last_synced: Optional[datetime] = None
    is_active: bool

    class Config:
        from_attributes = True


class PlaylistClipAssociationCreate(BaseModel):
    playlist_id: UUID
    clip_id: UUID
    relative_index: int = 0


class PlaylistClipAssociationResponse(BaseModel):
    id: UUID
    playlist_id: UUID
    clip_id: UUID
    relative_index: int
    added_at: datetime

    class Config:
        from_attributes = True


class UserProfileCreate(BaseModel):
    user_id: UUID
    profile_id: UUID


class UserProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    profile_id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProfileClipCreate(BaseModel):
    profile_id: UUID
    clip_id: UUID


class ProfileClipResponse(BaseModel):
    id: UUID
    profile_id: UUID
    clip_id: UUID
    is_active: bool
    added_at: datetime

    class Config:
        from_attributes = True


class ProfilePlaylistCreate(BaseModel):
    profile_id: UUID
    playlist_id: UUID


class ProfilePlaylistResponse(BaseModel):
    id: UUID
    profile_id: UUID
    playlist_id: UUID
    is_active: bool
    added_at: datetime

    class Config:
        from_attributes = True