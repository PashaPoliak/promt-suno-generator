from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from ...database.session import get_db
from ...models import dtos
from ...models.database import Profile, UserProfile, ProfileClip, ProfilePlaylist, Clip, Playlist as PlaylistModel
from sqlalchemy import asc, desc

router = APIRouter()


@router.get("/", response_model=List[dtos.ProfileResponse])
def get_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    profiles = db.query(Profile).offset(skip).limit(limit).all()
    return profiles


@router.get("/{profile_id}", response_model=dtos.ProfileResponse)
def get_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/handle/{handle}", response_model=dtos.ProfileResponse)
def get_profile_by_handle(handle: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.handle == handle).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/", response_model=dtos.ProfileResponse)
def create_profile(profile: dtos.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


# Enhanced profile endpoint with clips and playlists
@router.get("/handle/{handle}/", response_model=dtos.ProfileWithContentResponse)
def get_profile_with_content(
    handle: str,
    playlists_sort_by: str = Query("created_at", description="Sort playlists by: created_at, upvote_count, etc."),
    clips_sort_by: str = Query("created_at", description="Sort clips by: created_at, upvote_count, etc."),
    include_hooks: bool = Query(False, description="Include hooks in response"),
    db: Session = Depends(get_db)
):
    # Get the profile by handle
    profile = db.query(Profile).filter(Profile.handle == handle).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Get clips associated with this profile
    profile_clip_associations = db.query(ProfileClip).filter(ProfileClip.profile_id == profile.id).all()
    clip_ids = [assoc.clip_id for assoc in profile_clip_associations]
    clips_query = db.query(Clip).filter(Clip.id.in_(clip_ids))
    
    # Apply sorting for clips
    if clips_sort_by == "upvote_count":
        clips_query = clips_query.order_by(desc(Clip.upvote_count))
    elif clips_sort_by == "created_at":
        clips_query = clips_query.order_by(desc(Clip.created_at))
    elif clips_sort_by == "play_count":
        clips_query = clips_query.order_by(desc(Clip.play_count))
    else:
        clips_query = clips_query.order_by(desc(Clip.created_at))  # default
    
    clips = clips_query.all()
    
    # Get playlists associated with this profile
    profile_playlist_associations = db.query(ProfilePlaylist).filter(ProfilePlaylist.profile_id == profile.id).all()
    playlist_ids = [assoc.playlist_id for assoc in profile_playlist_associations]
    playlists_query = db.query(PlaylistModel).filter(PlaylistModel.id.in_(playlist_ids))
    
    # Apply sorting for playlists
    if playlists_sort_by == "upvote_count":
        playlists_query = playlists_query.order_by(desc(PlaylistModel.upvote_count))
    elif playlists_sort_by == "created_at":
        playlists_query = playlists_query.order_by(desc(PlaylistModel.created_at))
    elif playlists_sort_by == "play_count":
        playlists_query = playlists_query.order_by(desc(PlaylistModel.play_count))
    elif playlists_sort_by == "asc":
        playlists_query = playlists_query.order_by(asc(PlaylistModel.name))
    else:
        playlists_query = playlists_query.order_by(desc(PlaylistModel.created_at))  # default
    
    playlists = playlists_query.all()
    
    # Create response with profile, clips and playlists
    profile_response = dtos.ProfileWithContentResponse.from_orm(profile)
    # We need to manually add clips and playlists to the response
    profile_response.clips = [dtos.ClipResponse.from_orm(clip) for clip in clips]
    from ...models.dtos import PlaylistEntity
    profile_response.playlists = [PlaylistEntity.from_orm(playlist) for playlist in playlists]
    
    return profile_response


@router.put("/{profile_id}", response_model=dtos.ProfileResponse)
def update_profile(
    profile_id: str,
    profile: dtos.ProfileCreate,
    db: Session = Depends(get_db)
):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in profile.dict().items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.delete("/{profile_id}")
def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(profile)
    db.commit()
    return {"message": "Profile deleted successfully"}