from pydantic import BaseModel
from typing import Optional

class BaseProfile(BaseModel):
    full_name: str
    username: str
    photo_url: Optional[str] = None
    university: str
    faculty: str
    major: str
    points: int = 0


class ProfileCreate(BaseProfile):
    pass

 
class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    university: Optional[str] = None
    faculty: Optional[str] = None
    major: Optional[str] = None
    points: Optional[int] = None


# validation on response i take a baseprofile and add id to it
class ProfileOut(BaseProfile):
    id: int

    class Config:
        orm_mode = True
