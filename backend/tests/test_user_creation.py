import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from backend.app.utils.setup_sample_data import SunoAPIParser
from database.session import SessionLocal
from models.database import engine, Base, User
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    # Check users before
    users_before = db.query(User).count()
    print(f'Users before: {users_before}')
    
    parser = SunoAPIParser(db)
    result = parser.parse_and_save_profile('fotballpiraten')
    print('Saved result:', result)
    
    # Check users after
    users_after = db.query(User).count()
    print(f'Users after: {users_after}')
    
    db.commit()
    
    # Now let's verify by querying users directly
    users = db.query(User).all()
    print(f"Direct query found {len(users)} users")
    for user in users:
        print(f"User: {user.username} (ID: {user.id})")
        
except Exception as e:
    db.rollback()
    print(f'Error: {e}')
    import traceback
    traceback.print_exc()
finally:
    db.close()