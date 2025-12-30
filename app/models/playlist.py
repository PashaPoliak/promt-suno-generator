from pydantic import BaseModel, ConfigDict
from typing import Any, List, Optional
from datetime import datetime
from models.clip import ClipSlimDTO, ClipBaseDTO


class PlaylistDTO(BaseModel):
    id: str
    name: str
    handle: str
    description: Optional[str]
    image_url: Optional[str]
    clips: List[ClipBaseDTO]


class PlaylistEntity(BaseModel):
    id: str
    name: str
    handle: str
    description: Optional[str]
    image_url: Optional[str]
    clips: List[ClipSlimDTO] = []    
    model_config = ConfigDict(from_attributes=True)


class PlaylistCreate(BaseModel):
    id: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    upvote_count: int
    play_count: int
    song_count: int
    is_public: bool


class PlaylistResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    upvote_count: int
    play_count: int
    song_count: int
    is_public: bool
    clips: List[Any] = []
    
    model_config = ConfigDict(from_attributes=True)


class PlaylistEntityCreate(BaseModel):
    id: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    upvote_count: int
    play_count: int
    song_count: int
    is_public: bool


class PlaylistClipAssociationCreate(BaseModel):
    playlist_id: str
    clip_id: str
    relative_index: int = 0


class PlaylistClipAssociationResponse(BaseModel):
    id: str
    playlist_id: str
    clip_id: str
    relative_index: int
    added_at: datetime
    
    model_config = ConfigDict(from_attributes=True)