from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Routes
from app.routes import google_oauth
from app.routes import user_routes

app = FastAPI()

# ✅ CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React CRA
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register Routes
app.include_router(google_oauth.router, prefix="/oauth")
app.include_router(user_routes.router, prefix="/user")

# ✅ Serve uploaded images
app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")

# ✅ Root check
@app.get("/")
def root():
    return {"msg": "OAuth service running"}