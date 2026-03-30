from starlette.middleware.sessions import SessionMiddleware

from src.config.settings import settings


def register_sessions(app):
    app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)
