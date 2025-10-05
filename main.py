from fastapi import FastAPI
from core.db import Base, engine
from apps.auth.models.user import User, Invite, UserSession 
from core.config import settings
from core.session import SessionLocal
from apps.auth.api.auth import router 
from apps.profile.api.profile import router_profile
from apps.auth.api.users import router_users
from alembic import context
from fastapi.middleware.cors import CORSMiddleware

# ✅ CORS middleware to prevent 403 due to missing X-Requested-With
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://replit.com/@kareemalaa1/TopicX"],       # You can change this to ["http://localhost:3000"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)
app.include_router(router_users)
app.include_router(router_profile)