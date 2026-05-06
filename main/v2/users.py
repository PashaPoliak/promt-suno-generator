from fastapi import APIRouter
from .utils import read_json_file
from fastapi import HTTPException

USER_FILE = "follow.json"

router = APIRouter()


@router.get("")
def get_users_v2():
    user_data = read_json_file(str(USER_FILE))
    if user_data is None:
        raise HTTPException(status_code=404, detail="User data not found")
    return [user_data] if user_data else []


@router.get("/{user_id}")
def get_user_by_id_v2(user_id: str):
    user_data = read_json_file(str(USER_FILE))
    
    if user_data is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
