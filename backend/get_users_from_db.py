from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    handle = Column(String)
    display_name = Column(String)
    avatar_image_url = Column(String)

engine = create_engine("sqlite:///suno.db")
SessionLocal = sessionmaker(bind=engine)

def get_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users

if __name__ == "__main__":
    for u in get_users():
        print(u.id, u.handle, u.display_name)
