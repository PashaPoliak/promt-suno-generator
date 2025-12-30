from fastapi import APIRouter, HTTPException
from .utils import read_json_file, read_json_from_folder

PROFILES_DIR = "json/profiles"

router = APIRouter()


@router.get("")
def get_profiles_v2():
    profile_data = read_json_from_folder(PROFILES_DIR)

    if profile_data is None:
        raise HTTPException(status_code=404, detail=f"Profiles not found")

    return profile_data
    

@router.get("/{profile_handle}")
def get_profile_by_handle_v2(profile_handle: str):
    file_path =  f"{PROFILES_DIR}/{profile_handle}.json"
    profile_data = read_json_file(file_path)
    
    if profile_data is None:
        raise HTTPException(status_code=404, detail=f"Profile '{profile_handle}' not found")
    
    return profile_data
