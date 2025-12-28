from fastapi import FastAPI, Depends, HTTPException
from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy import JSON, create_engine, Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, Session
from pydantic import BaseModel, ConfigDict
import requests

engine = create_engine("sqlite:///suno.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

playlist_clips = Table(
    "playlist_clips", Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id"), primary_key=True),
    Column("clip_id", String, ForeignKey("clips.id"), primary_key=True),
)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String, primary_key=True)
    handle = Column(String, unique=True)
    display_name = Column(String)
    profile_description = Column(Text)
    avatar_image_url = Column(String)
    clips = relationship("ClipSlim", back_populates="profile", cascade="all, delete-orphan")
    full_clips = relationship("Clip", back_populates="profile", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="profile", cascade="all, delete-orphan")

class ClipSlim(Base):
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
    profile = relationship("Profile", back_populates="clips")
    playlists = relationship("Playlist", secondary=playlist_clips, back_populates="clips")

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
    clips = relationship("ClipSlim", secondary=playlist_clips, back_populates="playlists")

Base.metadata.create_all(engine)





class ClipSlimSlimDTO(BaseModel):
    id: str
    title: str
    status: str
    play_count: int
    upvote_count: int
    audio_url: Optional[str]
    video_url: Optional[str]
    image_url: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PlaylistDTO(BaseModel):
    id: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    upvote_count: int
    play_count: int
    song_count: int
    is_public: bool
    clips: List[ClipSlimSlimDTO] = []

class ProfileDTO(BaseModel):
    id: str
    handle: str
    display_name: str
    profile_description: Optional[str]
    avatar_image_url: Optional[str]
    clips: List[ClipSlimSlimDTO] = []
    playlists: List[PlaylistDTO] = []

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def fetch_clip_from_suno(clip_id: str) -> dict:
    url = f"https://studio-api.prod.suno.com/api/clip/{clip_id}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def fetch_profile_from_suno(handle: str) -> dict:
    url = f"https://studio-api.prod.suno.com/api/profiles/{handle}"
    params = {"playlists_sort_by": "upvote_count", "clips_sort_by": "created_at"}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def save_profile(db: Session, data: dict):
    profile = db.query(Profile).filter(Profile.id == data["user_id"]).first()
    if not profile:
        profile = Profile(
            id=data["user_id"],
            handle=data["handle"],
            display_name=data["display_name"],
            profile_description=data.get("profile_description"),
            avatar_image_url=data.get("avatar_image_url")
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    for c in data.get("clips", []):
        if not c.get("id"):
            continue
        clip = db.query(ClipSlim).filter(ClipSlim.id == c["id"]).first()
        if not clip:
            clip = ClipSlim(
                id=c["id"],
                profile=profile,
                title=c.get("title"),
                status=c.get("status"),
                play_count=c.get("play_count", 0),
                upvote_count=c.get("upvote_count", 0),
                audio_url=c.get("audio_url"),
                video_url=c.get("video_url"),
                image_url=c.get("image_url"),
                created_at=datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
            )
            db.add(clip)

    for p in data.get("playlists", []):
        if not p.get("id"):
            continue
        playlist = db.query(Playlist).filter(Playlist.id == p["id"]).first()
        if not playlist:
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
            db.add(playlist)
    db.commit()


class Clip(Base):
    __tablename__ = "full_clips"
    id = Column(String, primary_key=True)
    profile_id = Column(String, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="full_clips")
    status = Column(String)
    title = Column(String)
    play_count = Column(Integer)
    upvote_count = Column(Integer)
    allow_comments = Column(Boolean)
    entity_type = Column(String)
    video_url = Column(String)
    audio_url = Column(String)
    image_url = Column(String)
    image_large_url = Column(String)
    major_model_version = Column(String)
    model_name = Column(String)
    clip_metadata = Column(JSON)
    caption = Column(Text)
    type = Column(String)
    duration = Column(Integer)
    refund_credits = Column(Boolean)
    stream = Column(Boolean)
    make_instrumental = Column(Boolean)
    task = Column(String)
    can_remix = Column(Boolean)
    is_remix = Column(Boolean)
    priority = Column(Integer)
    has_stem = Column(Boolean)
    video_is_stale = Column(Boolean)
    uses_latest_model = Column(Boolean)
    model_badges = Column(JSON)
    is_liked = Column(Boolean)
    user_id = Column(String)
    display_name = Column(String)
    handle = Column(String)
    is_handle_updated = Column(Boolean)
    avatar_image_url = Column(String)
    is_trashed = Column(Boolean)
    created_at = Column(DateTime)
    is_public = Column(Boolean)
    is_following_creator = Column(Boolean)
    explicit = Column(Boolean)
    comment_count = Column(Integer)
    flag_count = Column(Integer)
    is_contest_clip = Column(Boolean)
    has_hook = Column(Boolean)
    batch_index = Column(Integer)
    profile = relationship("Profile", back_populates="full_clips")

class ClipDTO(BaseModel):
    id: str
    status: str
    title: str
    play_count: int
    upvote_count: int
    allow_comments: Optional[bool]
    entity_type: Optional[str]
    video_url: Optional[str]
    audio_url: Optional[str]
    image_url: Optional[str]
    image_large_url: Optional[str]
    major_model_version: Optional[str]
    model_name: Optional[str]
    clip_metadata: Optional[Dict[str, Any]]
    caption: Optional[str]
    type: Optional[str]
    duration: Optional[int]
    refund_credits: Optional[bool]
    stream: Optional[bool]
    make_instrumental: Optional[bool]
    task: Optional[str]
    can_remix: Optional[bool]
    is_remix: Optional[bool]
    priority: Optional[int]
    has_stem: Optional[bool]
    video_is_stale: Optional[bool]
    uses_latest_model: Optional[bool]
    model_badges: Optional[Dict[str, Any]]
    is_liked: Optional[bool]
    user_id: Optional[str]
    display_name: Optional[str]
    handle: Optional[str]
    is_handle_updated: Optional[bool]
    avatar_image_url: Optional[str]
    is_trashed: Optional[bool]
    created_at: datetime
    is_public: Optional[bool]
    is_following_creator: Optional[bool]
    explicit: Optional[bool]
    comment_count: Optional[int]
    flag_count: Optional[int]
    is_contest_clip: Optional[bool]
    has_hook: Optional[bool]
    batch_index: Optional[int]

def save_clip(db_session, data: dict):
    clip = db_session.query(Clip).filter(Clip.id == data["id"]).first()
    if not clip:
        profile = db_session.query(Profile).filter(Profile.id == data.get("user_id")).first()
        clip = Clip(
            id=data["id"],
            profile=profile,
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
            duration=data.get("duration"),
            refund_credits=data.get("refund_credits"),
            stream=data.get("stream"),
            make_instrumental=data.get("make_instrumental"),
            task=data.get("task"),
            can_remix=data.get("can_remix"),
            is_remix=data.get("is_remix"),
            priority=data.get("priority"),
            has_stem=data.get("has_stem"),
            video_is_stale=data.get("video_is_stale"),
            uses_latest_model=data.get("uses_latest_model"),
            model_badges=data.get("model_badges"),
            is_liked=data.get("is_liked"),
            user_id=data.get("user_id"),
            display_name=data.get("display_name"),
            handle=data.get("handle"),
            is_handle_updated=data.get("is_handle_updated"),
            avatar_image_url=data.get("avatar_image_url"),
            is_trashed=data.get("is_trashed"),
            created_at=datetime.fromisoformat(data["created_at"].replace("Z", "+00:00")),
            is_public=data.get("is_public"),
            is_following_creator=data.get("is_following_creator"),
            explicit=data.get("explicit"),
            comment_count=data.get("comment_count"),
            flag_count=data.get("flag_count"),
            is_contest_clip=data.get("is_contest_clip"),
            has_hook=data.get("has_hook"),
            batch_index=data.get("batch_index"),
        )
        db_session.add(clip)
        db_session.commit()


@app.get("/api/v1/profiles/{handle}", response_model=ProfileDTO)
def get_profile(handle: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.handle == handle).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Convert SQLAlchemy objects to primitive types for Pydantic
    return ProfileDTO(
        id=str(profile.id) if profile.id is not None else "",
        handle=str(profile.handle) if profile.handle is not None else "",
        display_name=str(profile.display_name) if profile.display_name is not None else "",
        profile_description=str(profile.profile_description) if profile.profile_description is not None else None,
        avatar_image_url=str(profile.avatar_image_url) if profile.avatar_image_url is not None else None,
        clips=[
            ClipSlimSlimDTO(
                id=str(c.id) if c.id is not None else "",
                title=str(c.title) if c.title is not None else "",
                status=str(c.status) if c.status is not None else "",
                play_count=int(c.play_count) if c.play_count is not None else 0,
                upvote_count=int(c.upvote_count) if c.upvote_count is not None else 0,
                audio_url=str(c.audio_url) if c.audio_url is not None else None,
                video_url=str(c.video_url) if c.video_url is not None else None,
                image_url=str(c.image_url) if c.image_url is not None else None,
                created_at=c.created_at
            ) for c in profile.clips
        ],
        playlists=[
            PlaylistDTO(
                id=str(p.id) if p.id is not None else "",
                name=str(p.name) if p.name is not None else "",
                description=str(p.description) if p.description is not None else None,
                image_url=str(p.image_url) if p.image_url is not None else None,
                upvote_count=int(p.upvote_count) if p.upvote_count is not None else 0,
                play_count=int(p.play_count) if p.play_count is not None else 0,
                song_count=int(p.song_count) if p.song_count is not None else 0,
                is_public=bool(p.is_public) if p.is_public is not None else False,
                clips=[]
            ) for p in profile.playlists
        ]
    )

@app.get("/api/v1/playlist/{playlist_id}", response_model=PlaylistDTO)
def get_playlist(playlist_id: str, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
    
    # Using getattr to force value conversion
    return PlaylistDTO(
        id=getattr(playlist, 'id', ''),
        name=getattr(playlist, 'name', ''),
        description=getattr(playlist, 'description', None),
        image_url=getattr(playlist, 'image_url', None),
        upvote_count=getattr(playlist, 'upvote_count', 0),
        play_count=getattr(playlist, 'play_count', 0),
        song_count=getattr(playlist, 'song_count', 0),
        is_public=getattr(playlist, 'is_public', False),
        clips=[
            ClipSlimSlimDTO(
                id=getattr(c, 'id', ''),
                title=getattr(c, 'title', ''),
                status=getattr(c, 'status', ''),
                play_count=getattr(c, 'play_count', 0),
                upvote_count=getattr(c, 'upvote_count', 0),
                audio_url=getattr(c, 'audio_url', None),
                video_url=getattr(c, 'video_url', None),
                image_url=getattr(c, 'image_url', None),
                created_at=c.created_at
            ) for c in playlist.clips
        ]
    )

