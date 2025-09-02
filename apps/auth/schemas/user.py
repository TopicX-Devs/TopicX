from pydantic import BaseModel , EmailStr


class SuperUserRequest(BaseModel):
    mail: EmailStr
    password: str

class SuperUserResponse(BaseModel):
    id: int
    role: str = "admin"
    mail: EmailStr
    token: str