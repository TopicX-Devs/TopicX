from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.db import get_db
import secrets, string
from apps.auth.schemas.user import GenerateRequest
from apps.auth.models.user import User
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
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


# ----- Endpoint -----
@router_users.post('/generate')
def generate_users(
    req: GenerateRequest,
    db: Session = Depends(get_db),
    user = Depends(role_required(["admin"]))  # فقط الأدمن يقدر يستخدمها
):
    if req.role not in ["admin", "sub_admin", "professor", "assistant", "student"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    if req.role == "sub_admin":
        existing_subs = db.query(User).filter(User.role == req.role).count()
        if existing_subs + req.count > 3:
            raise HTTPException(status_code=400, detail="Max 3 sub-admins allowed")

    users = []
    for i in range(req.count):
        email = f"{req.role}_{secrets.token_hex(4)}@TopicX.com"
        password = generate_password()
        user_obj = User(email=email, hashed_password=password, role=req.role)
        db.add(user_obj)
        users.append({"email": email, "password": password, "role": req.role})

    db.commit()
    return {"generated": users}
