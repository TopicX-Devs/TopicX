from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.db import get_db
import secrets, string
from apps.auth.schemas.user import GenerateRequest , ResetPasswordRequest
from apps.auth.models.user import User
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from core.security import hash_password , verify_password
from core.config import settings


router_users = APIRouter(prefix="/users", tags=["users"])

# ----- Auth Setup -----
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# decode token & get user info
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token is invalid")

# role check
def role_required(allowed_roles: list[str]):
    def wrapper(user = Depends(get_current_user)):
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden for role: {user['role']}"
            )
        return user
    return wrapper


# ----- Password Generator -----
def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


@router_users.post('/generate')
def generate_users(
    req: GenerateRequest,
    db: Session = Depends(get_db),
    user = Depends(role_required(["admin", "sub_admin"]))  
):
    # 1- حدد الصلاحيات حسب مين بيطلب
    allowed_roles = ["student", "professor", "assistant"]
    if user["role"] == "admin":
        allowed_roles = ["admin", "sub_admin", "professor", "assistant", "student"]

    # 2- لو الـ role المطلوب مش مسموح للي بيطلب → Error
    if req.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{user['role']} not allowed to create {req.role}"
        )

    # 3- تحديد سقف الـ sub_admins = 3
    if req.role == "sub_admin":
        existing_subs = db.query(User).filter(User.role == req.role).count()
        if existing_subs + req.count > 3:
            raise HTTPException(status_code=400, detail="Max 3 sub-admins allowed")

    # 4- إنشاء المستخدمين
    user_data = [] # create a unnecessary list for only response
    user_response = []
    for i in range(req.count):
        email = f"{req.role}_{secrets.token_hex(4)}@topicx.com"
        password = generate_password()
        
        user_dict = {
            'email':email,
            'hashed_password':hash_password(password),
            'role':req.role,
            'must_change_password':True  # ✅ أول مرة يدخل لازم يغير الباسورد
        }
        
        user_data.append(user_dict)
        user_response.append({"email": email, "password": password , "role" : req.role})
    
    db.bulk_insert_mappings(User, user_data)
    db.commit()
    return {"generated": user_response }

# reset password
@router_users.post("/reset-password")
def reset_password(
    req: ResetPasswordRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    db_user = db.query(User).filter(User.email == user["email"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(req.old_password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password incorrect")

    db_user.hashed_password = hash_password(req.new_password)
    db_user.must_change_password = False
    db.commit()
    return {"message": "Password updated successfully"}