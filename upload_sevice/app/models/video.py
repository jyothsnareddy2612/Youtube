import uuid
from sqlalchemy import Column, String
from app.db.database import Base

class Video(Base):
    __tablename__ = "videosnew"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))  # 🔥 FIX
    title = Column(String)
    file_path = Column(String)
    status = Column(String)
    master_playlist = Column(String)
    error = Column(String)