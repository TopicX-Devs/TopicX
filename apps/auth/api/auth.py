from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from apps.auth.schemas.user import SuperUserRequest, SuperUserResponse , TokenRequest
from apps.auth.crud import auth as crud_auth
from core.security import create_access_token, create_refresh_token
from datetime import datetime, timedelta
from core.config import settings
from jose import jwt, JWTError


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=SuperUserResponse)
def login(request: SuperUserRequest, db: Session = Depends(get_db)):
    user = crud_auth.authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token_access = create_access_token({"sub": user.email, "role": user.role})
    token_refresh = create_refresh_token({"sub": user.email, "role": user.role})
    crud_auth.create_session(db, user.id, token_refresh)

    return SuperUserResponse(
        id=user.id,
        role=user.role,
        mail=user.email,
        token_access=token_access,
        token_refresh=token_refresh
    )


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

    user = crud_auth.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # تحقق أن الـ refresh token موجود ولسه مش revoked
    session = crud_auth.get_session_by_token(db, refresh_token)
    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")

    # اعمل rotation
    crud_auth.revoke_session(db, refresh_token)
    new_access = create_access_token({"sub": user.email, "role": user.role})
    new_refresh = create_refresh_token({"sub": user.email, "role": user.role})
    crud_auth.create_session(db, user.id, new_refresh)

    return {"access_token": new_access, "refresh_token": new_refresh}

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    success = crud_auth.revoke_session(db, refresh_token)
    if not success:
        raise HTTPException(status_code=401, detail="Invalid token or already logged out")
    return {"message": "Logged out successfully"}


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

    user = crud_auth.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    crud_auth.revoke_all_sessions(db, user.id)
    return {"message": "All sessions revoked, user logged out everywhere."}