from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt, JWTError
from core.security import verify_password, create_access_token, create_refresh_token
from core.config import settings
from apps.auth.models.user import User, UserSession

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_session(db: Session, user_id: int, refresh_token: str):
    session = UserSession(
        user_id=user_id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(session)
    db.commit()
    return session

def revoke_session(db: Session, refresh_token: str):
    session = db.query(UserSession).filter_by(token=refresh_token , revoked=False).first()
    if not session:
        return False
    session.revoked = True
    db.commit()
    return True

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_session_by_token(db: Session, token: str):
    return db.query(UserSession).filter_by(token=token, revoked=False).first()

def revoke_all_sessions(db: Session, user_id: int):
    db.query(UserSession).filter(UserSession.user_id == user_id, UserSession.revoked == False).update(
        {"revoked": True}
    )
    db.commit()
