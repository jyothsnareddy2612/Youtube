from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found")

# Engine
engine = create_engine(DATABASE_URL)

# Session
SessionLocal = sessionmaker(bind=engine)

# ✅ ADD THIS (VERY IMPORTANT)
Base = declarative_base()