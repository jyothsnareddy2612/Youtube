from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.middleware.cors import register_cors
from src.api.middleware.sessions import register_sessions
from src.api.rest.routes.auth import router as auth_router
from src.api.rest.routes.search import router as search_router
from src.api.rest.routes.upload import router as upload_router
from src.api.rest.routes.videos import router as videos_router
from src.data.clients.database import Base, engine

app = FastAPI()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


register_sessions(app)
register_cors(app)

app.include_router(upload_router, prefix="/api")
app.include_router(videos_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")
