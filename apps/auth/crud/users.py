from sqlalchemy.orm import Session
import secrets, string
from apps.auth.models.user import User
from core.security import hash_password, verify_password

def generate_password(length=10):
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def create_users(db: Session, role: str, count: int):
    user_data = []
    user_response = []
    for _ in range(count):
        email = f"{role}_{secrets.token_hex(4)}@topicx.com"
        password = generate_password()
        user_dict = {
            "email": email,
            "hashed_password": hash_password(password),
            "role": role,
            "must_change_password": True
        }
        user_data.append(user_dict)
        user_response.append({"email": email, "password": password, "role": role})

    db.bulk_insert_mappings(User, user_data)
    db.commit()
    return user_response

def reset_user_password(db: Session, user: User, old_password: str, new_password: str):
    if not verify_password(old_password, user.hashed_password):
        return False
    user.hashed_password = hash_password(new_password)
    user.must_change_password = False
    db.commit()
    return True
