from core.db import engine
from apps.auth.models.user import User
from core.security import hash_password
from core.session import SessionLocal

# open session with database
db = SessionLocal()

# check if this admin is exsist really or no 
exsiting_admin  = db.query(User).filter(User.role == "admin").first()
if exsiting_admin:
    print(f"Admin already exists: {existing_admin.email}")
else:
    # define the admin account
    admin_email = "admin@topicx.com"
    admin_password = "adminTopicX123!"

    hashed_pwd = hash_password(admin_password)

    admin_user = User(
        email=admin_email,
        hashed_password=hashed_pwd,
        role="admin",
        must_change_password=True
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    print("Admin created successfully!")
    print("Use the following credentials to login:")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")