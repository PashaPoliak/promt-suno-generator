from fastapi import APIRouter, HTTPException
from .utils import read_json_file, read_json_from_folder

CLIPS_DIR = "json/clips"

router = APIRouter()


@router.get("")
def get_clips_v2():
    clips_data = read_json_from_folder(CLIPS_DIR)
    if clips_data is None:
        raise HTTPException(status_code=404, detail="Clip data not found")
    return clips_data


@router.get("/{clip_id}")
def get_clip_by_id_v2(clip_id: str):
    file_path =  f"{CLIPS_DIR}/{clip_id}.json"
    clips_data = read_json_file(file_path)
    
    if clips_data is None:
        raise HTTPException(status_code=404, detail=f"Clip {clip_id} not found")
    return clips_data
