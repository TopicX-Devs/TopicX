from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from apps.auth.models.user import User
from apps.auth.schemas.user import SuperUserRequest, SuperUserResponse
from core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=SuperUserResponse)
def login(request: SuperUserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.mail).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.email, "role": user.role})
    
    return SuperUserResponse(
        id=user.id,
        role=user.role,
        mail=user.email,
        token=token
    )
