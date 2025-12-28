import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.api.api import app, fetch_profile_from_suno, save_profile
from backend.get_users_from_db import SessionLocal

if __name__ == "__main__":
    import uvicorn
    db = SessionLocal()
    profile = fetch_profile_from_suno("fotballpiraten")
    playlist_clips = fetch_all_Playlist_by_user_handle("fotballpiraten")
    playlist_clips = fetch_all_Playlist_by_ids(getPlaylistIds(profile))
    save_playlist_clips(db, playlist_clips)
    clips = fetch_all_clips_by_clips_ids(getClipsIds(playlist_clips))# getAllClipsIdsFromAllPlaylistClips
    save_clips(db, clips)
    save_profile(db, profile)
    db.close()
    uvicorn.run(app, host="127.0.0.1", port=8000)
