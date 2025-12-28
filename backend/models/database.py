# database.py
from sqlalchemy import Table, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.settings import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

playlist_clips = Table('playlist_clips', Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('clip_id', Integer, ForeignKey('clips.id')),
    Column('relative_index', Integer, nullable=True),
    Column('is_liked', Boolean, default=False),
    Column('added_at', DateTime, default=func.now()),
    Column('metadata', JSON, nullable=True)  # Store additional metadata
)


class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # UUID type in the database
    username = Column(String(100), unique=True)  # Optional field
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    clips = relationship("Clip", back_populates="user")
    playlists = relationship("Playlist", back_populates="user")
    
    def __repr__(self):
        return f"<User(id='{self.id}', username='{self.username}')>"


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Profile(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    handle = Column(String(100), unique=True, nullable=False, index=True)  # e.g., 'fotballpiraten'
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    external_user_id = Column(String(100))  # External user ID from Suno API
    display_name = Column(String(200))
    profile_description = Column(Text)
    avatar_image_url = Column(String(500))
    is_handle_updated = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)  # Added for profile verification
    is_active = Column(Boolean, default=True)
    stats = Column(JSON)  # Store profile stats as JSON
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="profiles")
    clips = relationship("Clip", back_populates="profile", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="profile", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Profile(handle='{self.handle}', display_name='{self.display_name}')>"

class Clip(Base):
    __tablename__ = 'clips'
    
    id = Column(Integer, primary_key=True)
    suno_clip_id = Column(String(100), unique=True, nullable=False, index=True)  # Suno's clip ID
    title = Column(String(300))
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=True)
    
    # Audio/Video URLs
    audio_url = Column(String(500))
    video_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    image_large_url = Column(String(500), nullable=True)
    
    # Stats
    play_count = Column(Integer, default=0)
    upvote_count = Column(Integer, default=0)
    downvote_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    flag_count = Column(Integer, default=0)
    skip_count = Column(Integer, default=0)
    
    # Clip metadata
    duration = Column(Integer)  # in seconds
    status = Column(String(50), default='complete')
    entity_type = Column(String(50), default='song_schema')
    major_model_version = Column(String(50), nullable=True)
    model_name = Column(String(100), nullable=True)
    metadata_json = Column(JSON, nullable=True)  # Store entire metadata JSON
    
    # Flags
    allow_comments = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    explicit = Column(Boolean, default=False)
    is_trashed = Column(Boolean, default=False)
    is_contest_clip = Column(Boolean, default=False)
    has_hook = Column(Boolean, default=False)
    refund_credits = Column(Boolean, default=False)
    stream = Column(Boolean, default=True)
    make_instrumental = Column(Boolean, default=False)
    can_remix = Column(Boolean, default=False)
    is_remix = Column(Boolean, default=False)
    has_stem = Column(Boolean, default=False)
    uses_latest_model = Column(Boolean, default=False)
    
    # Technical
    batch_index = Column(Integer, nullable=True)
    priority = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="clips")
    profile = relationship("Profile", back_populates="clips")
    playlists = relationship("Playlist", secondary=playlist_clips, back_populates="clips")
    
    def __repr__(self):
        return f"<Clip(title='{self.title}', suno_clip_id='{self.suno_clip_id}')>"

class Playlist(Base):
    __tablename__ = 'playlists'
    
    id = Column(Integer, primary_key=True)
    suno_playlist_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(300))
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=True)
    
    # Stats
    upvote_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)
    flag_count = Column(Integer, default=0)
    skip_count = Column(Integer, default=0)
    play_count = Column(Integer, default=0)
    song_count = Column(Integer, default=0)
    num_total_results = Column(Integer, default=0)
    
    # Metadata
    image_url = Column(String(500), nullable=True)
    entity_type = Column(String(50), default='playlist_schema')
    current_page = Column(Integer, default=1)
    next_cursor = Column(Text, nullable=True)
    
    # Flags
    is_owned = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    is_trashed = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    is_discover_playlist = Column(Boolean, default=False)
    
    # User info (from playlist owner)
    user_display_name = Column(String(200), nullable=True)
    user_handle = Column(String(100), nullable=True)
    user_avatar_image_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="playlists")
    profile = relationship("Profile", back_populates="playlists")
    clips = relationship("Clip", secondary=playlist_clips, back_populates="playlists")
    
    def __repr__(self):
        return f"<Playlist(name='{self.name}', suno_playlist_id='{self.suno_playlist_id}')>"


class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    tag_type = Column(String(50))  # 'genre', 'mood', 'style', 'instrument', 'voice'
    created_at = Column(DateTime, server_default=func.now())


class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    genre = Column(String(10))
    mood = Column(String(100))
    style = Column(String(100))
    instruments = Column(Text)
    voice_tags = Column(Text)
    lyrics_structure = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    category_id = Column(String(36), ForeignKey("categories.id"))
    created_by = Column(String(36), ForeignKey("users.id"))


class PromptTemplateTag(Base):
    __tablename__ = "prompt_template_tags"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    template_id = Column(String(36), ForeignKey("prompt_templates.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(String(36), ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class GeneratedPrompt(Base):
    __tablename__ = "generated_prompts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"))
    template_id = Column(String(36), ForeignKey("prompt_templates.id"))
    prompt_text = Column(Text, nullable=False)
    parameters = Column(JSON)  # Store additional parameters as JSON
    created_at = Column(DateTime, server_default=func.now())
    is_favorite = Column(Boolean, default=False)
    generation_result = Column(JSON)  # Store Suno API response if needed


class FavoritePrompt(Base):
    __tablename__ = "favorite_prompts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    prompt_id = Column(String(36), ForeignKey("generated_prompts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint('user_id', 'prompt_id', name='unique_user_prompt_favorite'),)

# Association table for user profiles (users can have multiple profiles)
class UserProfile(Base):
    __tablename__ = "user_profiles"  # Renamed to match actual table
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False) # Changed to Integer to match Profile.id
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint('user_id', 'profile_id', name='unique_user_profile'),)


# Association table for profile clips (profiles have clips)
class ProfileClip(Base):
    __tablename__ = "profile_clips"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)  # Changed to Integer to match Profile.id
    clip_id = Column(Integer, ForeignKey("clips.id", ondelete="CASCADE"), nullable=False)  # Changed to Integer to match Clip.id
    is_active = Column(Boolean, default=True)
    added_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint('profile_id', 'clip_id', name='unique_profile_clip'),)


# Association table for profile playlists (profiles have playlists)
class ProfilePlaylist(Base):
    __tablename__ = "profile_playlists"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)  # Changed to Integer to match Profile.id
    playlist_id = Column(Integer, ForeignKey("playlists.id", ondelete="CASCADE"), nullable=False)  # Changed to Integer to match Playlist.id
    is_active = Column(Boolean, default=True)
    added_at = Column(DateTime, server_default=func.now())
    
    __table_args__ = (UniqueConstraint('profile_id', 'playlist_id', name='unique_profile_playlist'),)
    