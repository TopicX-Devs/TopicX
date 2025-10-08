from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.auth.models.user import User, Invite, UserSession  # noqa: F401
from apps.profile.models.profile import Profile
from core.db import Base, engine
from core.config import settings
from core.session import SessionLocal

from apps.auth.models.user import User, Invite, UserSession
from apps.auth.api.auth import router
from apps.auth.api.users import router_users
from apps.profile.api.profile import router_profile

# ❗ مبدئيًا خليه هنا لحد ما تستخدم Alembic للمigrations
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# ✅ السماح للفرونت أو Postman بالوصول
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://f7b54561-8e7a-4a7b-9a22-4ddbf8180340-00-gq6mcn2rsx5c.janeway.replit.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ إضافة الـ routes
app.include_router(router)
app.include_router(router_users)
app.include_router(router_profile)

# ✅ تأكيد أن السيرفر شغال
@app.get("/")
def root():
  return {"message": f"{settings.PROJECT_NAME} backend is running ✅"}
