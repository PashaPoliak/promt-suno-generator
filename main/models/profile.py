from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from models.clip import ClipBaseDTO, ClipSlimDTO
from models.playlist import PlaylistBaseDTO, PlaylistDTO

class UserDTO(BaseModel):
    id: Optional[str] = None
    handle: Optional[str] = None
    display_name: Optional[str] = None
    avatar_image_url: Optional[str] = None

class ProfileDTO(BaseModel):
    id: Optional[str] = None
    handle: Optional[str] = None
    display_name: Optional[str] = None
    profile_description: Optional[str] = None
    avatar_image_url: Optional[str] = None
    clips: List[ClipSlimDTO]
    playlists: List[PlaylistDTO]
    model_config = ConfigDict(from_attributes=True)

class ProfileBaseDTO(BaseModel):
    id: Optional[str] = None
    handle: Optional[str] = None
    display_name: Optional[str] = None
    avatar_image_url: Optional[str] = None
    clips: List[ClipBaseDTO]
    playlists: List[PlaylistBaseDTO]
    model_config = ConfigDict(from_attributes=True)