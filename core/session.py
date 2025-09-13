from sqlalchemy.orm import sessionmaker
from core.db import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


