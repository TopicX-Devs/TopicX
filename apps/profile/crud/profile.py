from sqlalchemy.orm import Session
from ..models.profile import Profile
from ..schemas.profile import ProfileCreate , ProfileUpdate , ProfileOut


# create profile 
def create_profile(db:Session , profile_in : ProfileCreate , user_id : int):
    db_profile = Profile(
        user_id=user_id,
        full_name=profile_in.full_name,
        username=profile_in.username,
        photo_url=profile_in.photo_url,
        university=profile_in.university,
        faculty=profile_in.faculty,
        major=profile_in.major,
        points=profile_in.points,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile
    

# read profile 
def get_profile(db:Session , profile_id : int):
    return db.query(Profile).filter(Profile.id == profile_id).first()

def get_profiles(db:Session , skip : int = 0 , limit : int = 10):
    return db.query(Profile).offset(skip).limit(limit).all()

# update profile
def update_profile(db:Session , profile_id : int , profile_in : ProfileUpdate): 
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        return None

    for field , value in profile_in.dict(exclude_unset=True).items():
        setattr(db_profile , field , value)
    db.commit()
    db.refresh(db_profile)
    return db_profile

# delete profile
def delete_profile(db:Session , profile_id : int): 
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        return None
    db.delete(db_profile)
    db.commit()
    return db_profile

    