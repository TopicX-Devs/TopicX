from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.db import get_db
from apps.auth.schemas.user import GenerateRequest, ResetPasswordRequest
from apps.auth.crud import users as crud_users
from apps.auth.deps import get_current_user, role_required
from apps.auth.models.user import User

router_users = APIRouter(prefix="/users", tags=["users"])

@router_users.post('/generate')
def generate_users(
    req: GenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(["admin", "sub_admin"]))
):
    return {"generated": crud_users.create_users(db, req.role, req.count)}

@router_users.post("/reset-password")
def reset_password(
    req: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = crud_users.reset_user_password(db, current_user, req.old_password, req.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Old password incorrect")
    return {"message": "Password updated successfully"}
