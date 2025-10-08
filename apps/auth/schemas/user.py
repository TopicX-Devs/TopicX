from pydantic import BaseModel, EmailStr

# ----- Login -----
class SuperUserRequest(BaseModel):
    email: EmailStr
    password: str

class SuperUserResponse(BaseModel):
    id: int
    role: str
    mail: EmailStr
    token_access: str
    token_refresh: str

# ----- Token Operations -----
class TokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

# ----- User Generation -----
class GenerateRequest(BaseModel):
    role: str
    count: int

# ----- Password Management -----
class ResetPasswordRequest(BaseModel):
    old_password: str
    new_password: str

class AdminResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str
