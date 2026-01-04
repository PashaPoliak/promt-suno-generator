export interface MetadataDTO {
  tags?: string;
  prompt?: string;
  duration?: string;
}

export interface ClipBaseDTO {
  id: string;
  title: string;
  audio_url?: string;
  image_url?: string;
}

export interface ClipSlimDTO {
  id: string;
  title: string;
  audio_url?: string;
  video_url?: string;
  image_url?: string;
  metadata?: MetadataDTO;
}

export interface ClipDTO {
  id: string;
  title: string;
  video_url?: string;
  audio_url?: string;
  image_url?: string;
  image_large_url?: string;
  clip_metadata?: MetadataDTO;
  caption?: string;
  type?: string;
  duration?: number | string;
  task?: string;
  user_id?: string;
  display_name?: string;
  handle?: string;
  user_avatar_image_url?: string;
}

export interface PlaylistClipDTO {
  id: string;
  title: string;
  audio_url?: string;
  video_url?: string;
  image_url?: string;
  created_at: string;
  image_large_url?: string;
  clip_metadata?: MetadataDTO;
  caption?: string;
  type?: string;
  stream?: boolean;
  make_instrumental?: boolean;
  task?: string;
  can_remix?: boolean;
  is_remix?: boolean;
  priority?: number;
  has_stem?: boolean;
  video_is_stale?: boolean;
  uses_latest_model?: boolean;
  is_liked?: boolean;
  user_id?: string;
  display_name?: string;
  handle?: string;
  is_handle_updated?: boolean;
  avatar_image_url?: string;
  is_trashed?: boolean;
  is_public?: boolean;
  is_following_creator?: boolean;
  explicit?: boolean;
  comment_count?: number;
  flag_count?: number;
  is_contest_clip?: boolean;
  has_hook?: boolean;
}

export interface PlaylistDTO {
  id: string;
  name: string;
  handle: string;
 description?: string;
  image_url?: string;
  clips: ClipBaseDTO[];
}

export interface PlaylistEntity {
  id: string;
  name: string;
  handle: string;
  description?: string;
  image_url?: string;
  clips: ClipSlimDTO[];
}

export interface PlaylistCreate {
  id: string;
  name: string;
  description?: string;
  image_url?: string;
  upvote_count: number;
  play_count: number;
  song_count: number;
  is_public: boolean;
}

export interface PlaylistResponse {
  id: string;
  name: string;
  description?: string;
  image_url?: string;
  upvote_count: number;
  play_count: number;
  song_count: number;
  is_public: boolean;
  clips: any[];
}

export interface PlaylistEntityCreate {
  id: string;
  name: string;
  description?: string;
  image_url?: string;
  upvote_count: number;
  play_count: number;
  song_count: number;
  is_public: boolean;
}

export interface PlaylistClipAssociationCreate {
  playlist_id: string;
  clip_id: string;
  relative_index: number;
}

export interface PlaylistClipAssociationResponse {
  id: string;
  playlist_id: string;
  clip_id: string;
  relative_index: number;
  added_at: string;
}

export interface UserDTO {
  id?: string;
  handle?: string;
  display_name?: string;
  avatar_image_url?: string;
}

export interface ProfileDTO {
  id?: string;
  handle?: string;
  display_name?: string;
  profile_description?: string;
  avatar_image_url?: string;
  clips: ClipSlimDTO[];
  playlists: PlaylistDTO[];
}