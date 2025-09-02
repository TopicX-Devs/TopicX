from fastapi import FastAPI
from core.db import Base, engine
from apps.auth.models.user import User, Invite, Session 
from core.config import settings
from core.session import SessionLocal
from apps.auth.api.auth import router 

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(router)
