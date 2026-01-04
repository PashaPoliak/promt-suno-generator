import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.api import fetch_profile_from_suno
from config.session import get_db_sqlite
from models.entities import Base

def test_get_all_playlists():
    """Test the get_all_playlists functionality"""


if __name__ == "__main__":
    test_get_all_playlists()