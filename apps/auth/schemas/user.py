from pydantic import BaseModel , EmailStr


class SuperUserRequest(BaseModel):
    mail: EmailStr
    password: str

class SuperUserResponse(BaseModel):
    id: int
    role: str
    mail: EmailStr
    token_access: str
    token_refresh: str


class GenerateRequest(BaseModel):
    role: str
    count: int
    
class ResetPasswordRequest(BaseModel):
    old_password: str
    new_password: str