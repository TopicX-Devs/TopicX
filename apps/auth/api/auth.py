from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from apps.auth.models.user import User , UserSession
from apps.auth.schemas.user import SuperUserRequest, SuperUserResponse 
from core.security import verify_password, create_access_token , create_refresh_token
from datetime import datetime, timedelta
from core.config import settings
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["auth"])

# endpoint login with access token generated
@router.post("/login", response_model=SuperUserResponse)
def login(request: SuperUserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.mail).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token_access = create_access_token({"sub": user.email, "role": user.role})
    token_refresh = create_refresh_token({"sub": user.email, "role": user.role})
    
    # save refreshed token in sessions table
    session_table = UserSession(
        user_id=user.id,
        token=token_refresh,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(session_table)
    db.commit()

    return SuperUserResponse(
        id=user.id,
        role=user.role,
        mail=user.email,
        token_access=token_access,
        token_refresh=token_refresh
    )

# endpoint refresh long token and access token 
@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            refresh_token, 
            settings.REFRESH_SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # check refresh token exists in sessions table
    session = db.query(UserSession).filter_by(token=refresh_token, revoked=False).first()
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")

    # issue new tokens
    new_access = create_access_token({"sub": user.email, "role": user.role})
    new_refresh = create_refresh_token({"sub": user.email, "role": user.role})

    # optional: revoke old session (rotation)
    session.revoked = True
    new_session = UserSession(
        user_id=user.id,
        token=new_refresh,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(new_session)
    db.commit()

    return {"access_token": new_access, "refresh_token": new_refresh}

# endpoint Logout
@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    session = db.query(UserSession).filter_by(token=refresh_token, revoked=False).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid token or already logged out")
    
    session.revoked = True
    db.commit()
    return {"message": "Logged out successfully"}

# logout all sessions
@router.post("/logout-all")
def logout_all(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Revoke all sessions for this user
    db.query(UserSession).filter(UserSession.user_id == user.id, UserSession.revoked == False).update(
        {"revoked": True}
    )
    db.commit()

    return {"message": "All sessions revoked, user logged out everywhere."}


