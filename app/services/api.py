import requests
import json
import os

from config.logging_config import get_logger
logger = get_logger(__name__)

def save_to_file_json(folder_name, filename, data):
    folder = f"json/{folder_name}"
    logger.info(f"Saved: {folder_name}/{filename}")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{filename}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def fetch_clip_from_suno(clip_id: str) -> dict:
    try:
        url = "https://studio-api.prod.suno.com/api/clip/" + clip_id
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        logger.info(f"Successfully fetched clip: {clip_id}")
        save_to_file_json("clips", clip_id, r.json())
        return r.json()
    except Exception:
        logger.info(f"Fail fetched clip: {clip_id}")
        return {}

def fetch_profile_from_suno(handle: str) -> dict:
    try:
        url = "https://studio-api.prod.suno.com/api/profiles/" + handle
        params = {"playlists_sort_by": "upvote_count", "clips_sort_by": "created_at"}
        r = requests.get(url, params=params, timeout=3)
        r.raise_for_status()
        logger.info(f"Successfully fetched profile: {handle}")
        save_to_file_json("profiles", handle, r.json())
        return r.json()
    except Exception:
        logger.info(f"Fail fetched profile: {handle}")
        return {}

def fetch_playlist_from_suno(playlist_id: str) -> dict:
    try:
        url = f"https://studio-api.prod.suno.com/api/playlist/" + playlist_id
        r = requests.get(url, timeout=3)
        r.raise_for_status()
        logger.info(f"Successfully fetched playlist: {playlist_id}")
        save_to_file_json("playlists", playlist_id, r.json())
        return r.json()
    except Exception:
        logger.info(f"Fail fetched playlist: {playlist_id}")
        return {}
