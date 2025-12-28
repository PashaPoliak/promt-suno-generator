import logging
from datetime import datetime
import requests

from sqlalchemy import (
    create_engine,
    Table,
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    Text,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

playlist_clips = Table(
    "playlist_clips",
    Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id"), primary_key=True),
    Column("clip_id", String, ForeignKey("clips.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    handle = Column(String, unique=True, index=True)
    display_name = Column(String)
    avatar_image_url = Column(String)
    profiles = relationship("Profile", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    handle = Column(String, index=True)
    display_name = Column(String)
    profile_description = Column(Text)
    avatar_image_url = Column(String)
    user = relationship("User", back_populates="profiles")
    clips = relationship("Clip", back_populates="profile", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="profile", cascade="all, delete-orphan")

class Clip(Base):
    __tablename__ = "clips"
    id = Column(String, primary_key=True)
    profile_id = Column(String, ForeignKey("profiles.id"))
    title = Column(String)
    status = Column(String)
    play_count = Column(Integer)
    upvote_count = Column(Integer)
    audio_url = Column(String)
    video_url = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime)
    is_public = Column(Boolean)
    explicit = Column(Boolean)
    profile = relationship("Profile", back_populates="clips")

class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String, primary_key=True)
    profile_id = Column(String, ForeignKey("profiles.id"))
    name = Column(String)
    description = Column(Text)
    image_url = Column(String)
    upvote_count = Column(Integer)
    play_count = Column(Integer)
    song_count = Column(Integer)
    is_public = Column(Boolean)
    profile = relationship("Profile", back_populates="playlists")
    clips = relationship("Clip", secondary=playlist_clips)

engine = create_engine("sqlite:///suno.db")
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_and_save_profile(handle: str):
    url = f"https://studio-api.prod.suno.com/api/profiles/{handle}"
    params = {
        "playlists_sort_by": "upvote_count",
        "clips_sort_by": "created_at"
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    logger.info(data)
    session = SessionLocal()

    user = session.get(User, data["user_id"])
    if not user:
        user = User(
            id=data["user_id"],
            handle=data["handle"],
            display_name=data["display_name"],
            avatar_image_url=data.get("avatar_image_url")
        )
        session.add(user)

    profile = session.get(Profile, data["user_id"])
    if not profile:
        profile = Profile(
            id=data["user_id"],
            user=user,
            handle=data["handle"],
            display_name=data["display_name"],
            profile_description=data.get("profile_description"),
            avatar_image_url=data.get("avatar_image_url")
        )
        session.add(profile)

    profile.clips.clear()
    profile.playlists.clear()

    for c in data.get("clips", []):
        if not isinstance(c, dict) or "id" not in c:
            continue
        clip = Clip(
            id=c["id"],
            profile=profile,
            title=c.get("title"),
            status=c.get("status"),
            play_count=c.get("play_count", 0),
            upvote_count=c.get("upvote_count", 0),
            audio_url=c.get("audio_url"),
            video_url=c.get("video_url"),
            image_url=c.get("image_url"),
            created_at=datetime.fromisoformat(c["created_at"].replace("Z", "+00:00")),
            is_public=c.get("is_public", True),
            explicit=c.get("explicit", False)
        )
        session.add(clip)

    for p in data.get("playlists", []):
        if not isinstance(p, dict) or "id" not in p:
            continue
        playlist = Playlist(
            id=p["id"],
            profile=profile,
            name=p.get("name"),
            description=p.get("description"),
            image_url=p.get("image_url"),
            upvote_count=p.get("upvote_count", 0),
            play_count=p.get("play_count", 0),
            song_count=p.get("song_count", 0),
            is_public=p.get("is_public", True)
        )
        session.add(playlist)

    session.commit()
    session.close()

if __name__ == "__main__":
    parse_and_save_profile("fotballpiraten")
