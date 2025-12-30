from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class MongoClip(BaseModel):
    id: str
    title: str
    video_url: Optional[str] = None
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    image_large_url: Optional[str] = None
    clip_metadata: Optional[Dict[str, Any]] = None
    caption: Optional[str] = None
    type: Optional[str] = None
    duration: Optional[float] = None
    task: Optional[str] = None
    user_id: Optional[str] = None
    display_name: Optional[str] = None
    handle: Optional[str] = None
    user_avatar_image_url: Optional[str] = None
    status: Optional[str] = None
    play_count: Optional[int] = 0
    upvote_count: Optional[int] = 0
    allow_comments: Optional[bool] = None
    entity_type: Optional[str] = None
    major_model_version: Optional[str] = None
    model_name: Optional[str] = None
    refund_credits: Optional[bool] = None
    stream: Optional[bool] = None
    make_instrumental: Optional[bool] = None
    can_remix: Optional[bool] = None
    is_remix: Optional[bool] = None
    priority: Optional[int] = None
    has_stem: Optional[bool] = None
    video_is_stale: Optional[bool] = None
    uses_latest_model: Optional[bool] = None
    is_liked: Optional[bool] = False
    is_trashed: Optional[bool] = None
    is_public: Optional[bool] = None
    explicit: Optional[bool] = None
    comment_count: Optional[int] = None
    flag_count: Optional[int] = None
    is_contest_clip: Optional[bool] = None
    has_hook: Optional[bool] = None
    batch_index: Optional[int] = None
    is_pinned: Optional[bool] = None


class MongoPlaylist(BaseModel):
    id: str
    name: Optional[str] = None
    handle: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    upvote_count: Optional[int] = 0
    play_count: Optional[int] = 0
    song_count: Optional[int] = 0
    is_public: Optional[bool] = True
    entity_type: Optional[str] = None
    num_total_results: Optional[int] = None
    current_page: Optional[int] = None
    is_owned: Optional[bool] = None
    is_trashed: Optional[bool] = None
    is_hidden: Optional[bool] = None
    user_display_name: Optional[str] = None
    user_handle: Optional[str] = None
    user_avatar_image_url: Optional[str] = None
    dislike_count: Optional[int] = None
    flag_count: Optional[int] = None
    skip_count: Optional[int] = None
    is_discover_playlist: Optional[bool] = None
    next_cursor: Optional[str] = None
    clip_ids: List[str] = []


class MongoProfile(BaseModel):
    id: Optional[str] = None
    handle: Optional[str] = None
    display_name: Optional[str] = None
    profile_description: Optional[str] = None
    avatar_image_url: Optional[str] = None
    clip_ids: List[str] = []
    playlist_ids: List[str] = []