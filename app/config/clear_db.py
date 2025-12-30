import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.session import SessionLocal
from models.entities import *
from sqlalchemy import text

def clear_all_users():
    db = SessionLocal()
    try:
        db.query(PlaylistClip).delete()
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