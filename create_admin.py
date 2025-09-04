import secrets
import string
from apps.auth.models.user import User
from core.security import hash_password
from core.session import SessionLocal

db = SessionLocal()

def generate_password(length=12):
    # letters + nums + symbols
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(length))

# numbers of the admin you wanted 
num_admins = 3

for i in range(1, num_admins + 1):
    email = f"admin{i}@topicx.com"
    password = generate_password()

    existing_admin = db.query(User).filter(User.email == email).first()
    if existing_admin:
        print(f"Admin already exists: {existing_admin.email}")
        continue

    hashed_pwd = hash_password(password)
    admin_user = User(
        email=email,
        hashed_password=hashed_pwd,
        role="admin",
        must_change_password=True,
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    print("Admin created successfully!")
    print(f"Email: {email}")
    print(f"Password: {password}")

db.close()
