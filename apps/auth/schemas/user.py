from pydantic import BaseModel , EmailStr


class SuperUserRequest(BaseModel):
    mail: EmailStr
    password: str

class SuperUserResponse(BaseModel):
    id: int
    role: str = "admin"
    mail: EmailStr
    token_access: str
    token_refresh: str


class GenerateRequest(BaseModel):
    role: str
    count: int
    

