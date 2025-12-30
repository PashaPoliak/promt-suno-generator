from fastapi import APIRouter
from .utils import read_json_file

USER_FILE = "follow.json"

router = APIRouter()


@router.get("/")
def get_users_v2():
    """Get all users from JSON files"""
    user_data = read_json_file(str(USER_FILE))
    if user_data is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User data not found")
    return [user_data] if user_data else []


@router.get("/{user_id}")
def get_user_by_id_v2(user_id: str):
    """Get specific user by ID from JSON file"""
    user_data = read_json_file(str(USER_FILE))
    
    if user_data is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    # Check if the user_id matches
    if user_data.get("user_id") == user_id:
        return user_data
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")