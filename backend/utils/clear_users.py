from database.session import SessionLocal
from models.database import User, Profile, Clip, Playlist, UserProfile, ProfileClip, ProfilePlaylist
from models.database import engine, Base
from sqlalchemy import text

def clear_all_users():
    db = SessionLocal()
    try:
        # Delete related records first (due to foreign key constraints)
        db.query(UserProfile).delete()
        db.query(ProfileClip).delete()
        db.query(ProfilePlaylist).delete()
        db.query(Clip).delete()
        db.query(Playlist).delete()
        db.query(Profile).delete()
        db.query(User).delete()
        
        db.commit()
        print("All users and related data have been deleted from the database")
        
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_users()