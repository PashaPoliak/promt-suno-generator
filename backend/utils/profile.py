from typing import List, Optional
from datetime import datetime
import requests

from pydantic import BaseModel
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

API_URL = "https://studio-api.prod.suno.com/api/profiles"
PARAMS = {
    "playlists_sort_by": "upvote_count",
    "clips_sort_by": "created_at"
}

engine = create_engine("sqlite:///suno.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class ClipEntity(Base):
    __tablename__ = "clips"
    id = Column(String, primary_key=True)
    title = Column(String)
    status = Column(String)
    play_count = Column(Integer)
    upvote_count = Column(Integer)
    audio_url = Column(String)
    video_url = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime)
    profile_id = Column(String, ForeignKey("profiles.user_id"))

class ProfileEntity(Base):
    __tablename__ = "profiles"
    user_id = Column(String, primary_key=True)
    handle = Column(String)
    display_name = Column(String)
    profile_description = Column(Text)
    avatar_image_url = Column(String)
    clips = relationship("ClipEntity", cascade="all, delete-orphan")

Base.metadata.create_all(engine)

class ClipDTO(BaseModel):
    id: str
    title: str
    status: str
    play_count: int
    upvote_count: int
    audio_url: Optional[str]
    video_url: Optional[str]
    image_url: Optional[str]
    created_at: datetime

class ProfileDTO(BaseModel):
    user_id: str
    handle: str
    display_name: str
    profile_description: Optional[str]
    avatar_image_url: Optional[str]
    clips: List[ClipDTO]

def fetch_profile(profile: str) -> dict:
    r = requests.get(API_URL + profile, params=PARAMS, timeout=30)
    r.raise_for_status()
    return r.json()

def parse_profile(data: dict) -> ProfileDTO:
    clips = [
        ClipDTO(
            id=c["id"],
            title=c.get("title", ""),
            status=c.get("status", ""),
            play_count=c.get("play_count", 0),
            upvote_count=c.get("upvote_count", 0),
            audio_url=c.get("audio_url"),
            video_url=c.get("video_url"),
            image_url=c.get("image_url"),
            created_at=datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
        )
        for c in data.get("clips", [])
        if isinstance(c, dict) and "id" in c
    ]
    return ProfileDTO(
        user_id=data["user_id"],
        handle=data["handle"],
        display_name=data["display_name"],
        profile_description=data.get("profile_description"),
        avatar_image_url=data.get("avatar_image_url"),
        clips=clips
    )

def save_profile(dto: ProfileDTO):
    session = Session()
    profile = ProfileEntity(
        user_id=dto.user_id,
        handle=dto.handle,
        display_name=dto.display_name,
        profile_description=dto.profile_description,
        avatar_image_url=dto.avatar_image_url
    )
    for c in dto.clips:
        profile.clips.append(
            ClipEntity(
                id=c.id,
                title=c.title,
                status=c.status,
                play_count=c.play_count,
                upvote_count=c.upvote_count,
                audio_url=c.audio_url,
                video_url=c.video_url,
                image_url=c.image_url,
                created_at=c.created_at
            )
        )
    session.merge(profile)
    session.commit()
    session.close()

def ingest():
    raw = fetch_profile("fotballpiraten")
    dto = parse_profile(raw)
    save_profile(dto)

if __name__ == "__main__":
    ingest()
