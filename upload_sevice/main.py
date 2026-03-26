
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.upload import router as upload_router
from app.api.videos import router as videos_router
from app.auth.routes import router as auth_router
from app.core.config import settings
from app.db.database import Base, engine

app = FastAPI()

# ✅ AUTO CREATE TABLES (IMPORTANT FIX)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
        
        await conn.run_sync(Base.metadata.create_all)

# Session
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(upload_router, prefix="/api")
app.include_router(videos_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")

# Static
app.mount("/videos", StaticFiles(directory="videos"), name="videos")