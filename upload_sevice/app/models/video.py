from sqlalchemy import Column, Integer, String
from app.db.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # ✅ FIX
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)