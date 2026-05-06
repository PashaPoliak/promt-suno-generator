from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from models.clip import ClipSlimDTO, ClipBaseDTO

class PlaylistDTO(BaseModel):
    id: str
    name: str
    handle: str
    description: Optional[str]
    image_url: Optional[str]
    clips: List[ClipSlimDTO] = []    
    model_config = ConfigDict(from_attributes=True)

class PlaylistBaseDTO(BaseModel):
    id: str
    name: str
    image_url: Optional[str]
    clips: List[ClipBaseDTO] = []
    model_config = ConfigDict(from_attributes=True)
