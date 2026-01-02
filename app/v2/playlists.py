from fastapi import APIRouter, HTTPException
from .utils import read_json_file, read_json_from_folder

PLAYLISTS_DIR = "json/playlists"

router = APIRouter()


@router.get("")
def get_playlists_v2():
    playlists_data = read_json_from_folder(PLAYLISTS_DIR)
    if playlists_data is None:
        raise HTTPException(status_code=404, detail=f"Playlists not found")

    return playlists_data


@router.get("/{playlist_id}")
def get_playlist_by_id_v2(playlist_id: str):
    file_path =  f"{PLAYLISTS_DIR}/{playlist_id}.json"
    playlist_data = read_json_file(file_path)
    
    if playlist_data is None:
        raise HTTPException(status_code=404, detail=f"Playlist {playlist_id} not found")
    
    return playlist_data