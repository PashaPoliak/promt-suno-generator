from models.entities import Profile, Clip, Playlist
from sqlalchemy.orm import Session


class PlaylistDao:
    def __init__(self, db: Session):
        self.db = db

    def create_clip(self, clip_data):
            return Clip(
                id=clip_data["id"],
                title=clip_data.get("title"),
                status=clip_data.get("status"),
                play_count=clip_data.get("play_count", 0),
                upvote_count=clip_data.get("upvote_count", 0),
                audio_url=clip_data.get("audio_url"),
                video_url=clip_data.get("video_url"),
                image_url=clip_data.get("image_url"),
                image_large_url=clip_data.get("image_large_url"),
                allow_comments=clip_data.get("allow_comments"),
                entity_type=clip_data.get("entity_type"),
                major_model_version=clip_data.get("major_model_version"),
                model_name=clip_data.get("model_name"),
                clip_metadata=clip_data.get("metadata"),
                caption=clip_data.get("caption"),
                type=clip_data.get("type"),
                duration=str(clip_data.get("duration")) if clip_data.get("duration") is not None else None,
                refund_credits=clip_data.get("refund_credits"),
                stream=clip_data.get("stream"),
                make_instrumental=clip_data.get("make_instrumental"),
                can_remix=clip_data.get("can_remix"),
                is_remix=clip_data.get("is_remix"),
                priority=clip_data.get("priority"),
                has_stem=clip_data.get("has_stem"),
                video_is_stale=clip_data.get("video_is_stale"),
                uses_latest_model=clip_data.get("uses_latest_model"),
                is_liked=clip_data.get("is_liked"),
                user_id=clip_data.get("user_id"),
                display_name=clip_data.get("display_name"),
                handle=clip_data.get("handle"),
                is_handle_updated=clip_data.get("is_handle_updated"),
                avatar_image_url=clip_data.get("avatar_image_url"),
                is_trashed=clip_data.get("is_trashed"),
                is_public=clip_data.get("is_public"),
                explicit=clip_data.get("explicit"),
                comment_count=clip_data.get("comment_count"),
                flag_count=clip_data.get("flag_count"),
                is_contest_clip=clip_data.get("is_contest_clip"),
                has_hook=clip_data.get("has_hook"),
                batch_index=clip_data.get("batch_index"),
                is_pinned=clip_data.get("is_pinned")
            )

    def create_playlist(self, playlist_data):
        return Playlist(
            id=playlist_data["id"],
            name=playlist_data.get("name"),
            description=playlist_data.get("description"),
            image_url=playlist_data.get("image_url"),
            upvote_count=playlist_data.get("upvote_count", 0),
            play_count=playlist_data.get("play_count", 0),
            song_count=playlist_data.get("song_count", 0),
            is_public=playlist_data.get("is_public", True),
            entity_type=playlist_data.get("entity_type"),
            num_total_results=playlist_data.get("num_total_results"),
            current_page=playlist_data.get("current_page"),
            is_owned=playlist_data.get("is_owned"),
            is_trashed=playlist_data.get("is_trashed"),
            is_hidden=playlist_data.get("is_hidden"),
            user_display_name=playlist_data.get("user_display_name"),
            user_handle=playlist_data.get("user_handle"),
            user_avatar_image_url=playlist_data.get("user_avatar_image_url"),
            dislike_count=playlist_data.get("dislike_count"),
            flag_count=playlist_data.get("flag_count"),
            skip_count=playlist_data.get("skip_count"),
            is_discover_playlist=playlist_data.get("is_discover_playlist"),
            next_cursor=playlist_data.get("next_cursor")
        )


class ProfileDao:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(self, data):
        return Profile(
            id=data.get("id", data.get("user_id", data["handle"])),
            handle=data["handle"],
            display_name=data["display_name"],
            profile_description=data.get("profile_description"),
            avatar_image_url=data.get("avatar_image_url")
        )

    def create_playlist(self, p, profile):
        return Playlist(
            id=p["id"],
            profile_id=profile.id,
            name=p.get("name"),
            description=p.get("description"),
            image_url=p.get("image_url"),
            upvote_count=p.get("upvote_count", 0),
            play_count=p.get("play_count", 0),
            song_count=p.get("song_count", 0),
            is_public=p.get("is_public", True),
            entity_type=p.get("entity_type"),
            num_total_results=p.get("num_total_results"),
            current_page=p.get("current_page"),
            is_owned=p.get("is_owned"),
            is_trashed=p.get("is_trashed"),
            is_hidden=p.get("is_hidden"),
            user_display_name=p.get("user_display_name"),
            user_handle=p.get("user_handle"),
            user_avatar_image_url=p.get("user_avatar_image_url"),
            dislike_count=p.get("dislike_count"),
            flag_count=p.get("flag_count"),
            skip_count=p.get("skip_count"),
            is_discover_playlist=p.get("is_discover_playlist"),
            next_cursor=p.get("next_cursor")
        )

    def create_clip(self, c, profile):
        return Clip(
            id=c["id"],
            profile=profile,
            title=c.get("title"),
            status=c.get("status"),
            play_count=c.get("play_count", 0),
            upvote_count=c.get("upvote_count", 0),
            audio_url=c.get("audio_url"),
            video_url=c.get("video_url"),
            image_url=c.get("image_url"),
            image_large_url=c.get("image_large_url"),
            allow_comments=c.get("allow_comments"),
            entity_type=c.get("entity_type"),
            major_model_version=c.get("major_model_version"),
            model_name=c.get("model_name"),
            clip_metadata=c.get("metadata"),
            caption=c.get("caption"),
            type=c.get("type"),
            duration=str(c.get("duration")) if c.get("duration") is not None else None,
            refund_credits=c.get("refund_credits"),
            stream=c.get("stream"),
            make_instrumental=c.get("make_instrumental"),
            can_remix=c.get("can_remix"),
            is_remix=c.get("is_remix"),
            priority=c.get("priority"),
            has_stem=c.get("has_stem"),
            video_is_stale=c.get("video_is_stale"),
            uses_latest_model=c.get("uses_latest_model"),
            is_liked=c.get("is_liked"),
            user_id=c.get("user_id"),
            display_name=c.get("display_name"),
            handle=c.get("handle"),
            is_handle_updated=c.get("is_handle_updated"),
            avatar_image_url=c.get("avatar_image_url"),
            is_trashed=c.get("is_trashed"),
            is_public=c.get("is_public"),
            explicit=c.get("explicit"),
            comment_count=c.get("comment_count"),
            flag_count=c.get("flag_count"),
            is_contest_clip=c.get("is_contest_clip"),
            has_hook=c.get("has_hook"),
            batch_index=c.get("batch_index"),
            is_pinned=c.get("is_pinned")
        )
