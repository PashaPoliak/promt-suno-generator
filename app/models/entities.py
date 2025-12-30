from sqlalchemy import JSON, Column, String, Integer, Boolean, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


playlist_clips = Table(
    "playlist_clips", Base.metadata,
    Column("playlist_id", String, ForeignKey("playlists.id"), primary_key=True),
    Column("clip_id", String, ForeignKey("clips.id"), primary_key=True),
)


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(String(36), primary_key=True)
    handle = Column(String, unique=True)
    display_name = Column(String)
    profile_description = Column(Text)
    avatar_image_url = Column(String)
    clips = relationship("Clip", back_populates="profile", cascade="all, delete-orphan")
    playlists = relationship("Playlist", back_populates="profile", cascade="all, delete-orphan")


class Clip(Base):
    __tablename__ = "clips"
    id = Column(String(36), primary_key=True)
    profile_id = Column(String, ForeignKey("profiles.id"))
    title = Column(String)
    status = Column(String)
    play_count = Column(Integer)
    upvote_count = Column(Integer)
    audio_url = Column(String)
    video_url = Column(String)
    image_url = Column(String)
    image_large_url = Column(String)
    created_at = Column(DateTime)
    profile = relationship("Profile", back_populates="clips")
    playlists = relationship("Playlist", secondary=playlist_clips, back_populates="clips")
    allow_comments = Column(Boolean)
    entity_type = Column(String)
    major_model_version = Column(String)
    model_name = Column(String)
    clip_metadata = Column(JSON)
    caption = Column(Text)
    type = Column(String)
    duration = Column(String)
    refund_credits = Column(Boolean)
    stream = Column(Boolean)
    make_instrumental = Column(Boolean)
    can_remix = Column(Boolean)
    is_remix = Column(Boolean)
    priority = Column(Integer)
    has_stem = Column(Boolean)
    video_is_stale = Column(Boolean)
    uses_latest_model = Column(Boolean)
    is_liked = Column(Boolean)
    user_id = Column(String)
    display_name = Column(String)
    handle = Column(String)
    is_handle_updated = Column(Boolean)
    avatar_image_url = Column(String)
    is_trashed = Column(Boolean)
    is_public = Column(Boolean)
    explicit = Column(Boolean)
    comment_count = Column(Integer)
    flag_count = Column(Integer)
    is_contest_clip = Column(Boolean)
    has_hook = Column(Boolean)
    batch_index = Column(Integer)
    is_pinned = Column(Boolean)


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(String(36), primary_key=True)
    profile_id = Column(String, ForeignKey("profiles.id"))
    name = Column(String)
    description = Column(Text)
    image_url = Column(String)
    upvote_count = Column(Integer)
    play_count = Column(Integer)
    song_count = Column(Integer)
    is_public = Column(Boolean)
    profile = relationship("Profile", back_populates="playlists")
    clips = relationship("Clip", secondary=playlist_clips, back_populates="playlists")
    entity_type = Column(String)
    num_total_results = Column(Integer)
    current_page = Column(Integer)
    is_owned = Column(Boolean)
    is_trashed = Column(Boolean)
    is_hidden = Column(Boolean)
    user_display_name = Column(String)
    user_handle = Column(String)
    user_avatar_image_url = Column(String)
    dislike_count = Column(Integer)
    flag_count = Column(Integer)
    skip_count = Column(Integer)
    is_discover_playlist = Column(Boolean)
    next_cursor = Column(String)


class Category(Base):
    __tablename__ = "categories"
    id = Column(String(36), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime)
    
    
class Tag(Base):
    __tablename__ = "tags"
    id = Column(String(36), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    tag_type = Column(String)
    created_at = Column(DateTime)
    
    
class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True)
    username = Column(String, unique=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    
class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    id = Column(String(36), primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    genre = Column(String)
    mood = Column(String)
    style = Column(String)
    instruments = Column(String)
    voice_tags = Column(String)
    lyrics_structure = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    category_id = Column(String, ForeignKey("categories.id"))
    
    
class GeneratedPrompt(Base):
    __tablename__ = "generated_prompts"
    id = Column(String(36), primary_key=True)
    prompt_text = Column(Text, nullable=False)
    parameters = Column(JSON)
    is_favorite = Column(Boolean, default=False)
    generation_result = Column(JSON)
    created_at = Column(DateTime)
    user_id = Column(String, ForeignKey("users.id"))
    
    
class FavoritePrompt(Base):
    __tablename__ = "favorite_prompts"
    id = Column(String(36), primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    prompt_id = Column(String, ForeignKey("generated_prompts.id"), nullable=False)
    created_at = Column(DateTime)
    
    
class PromptTemplateTag(Base):
    __tablename__ = "prompt_template_tags"
    id = Column(String(36), primary_key=True)
    template_id = Column(String, ForeignKey("prompt_templates.id"))
    tag_id = Column(String, ForeignKey("tags.id"))
    created_at = Column(DateTime)


class PlaylistClip(Base):
    __tablename__ = "playlist_clips_entity"
    id = Column(String(36), primary_key=True)
    playlist_id = Column(String, ForeignKey("playlists.id"))
    clip_id = Column(String, ForeignKey("clips.id"))
    relative_index = Column(Integer)
