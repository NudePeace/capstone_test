from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime, date
from typing import Optional

# Request Models
class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=60)
    name: str = Field(..., min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=10)
    address: Optional[str] = Field(None, max_length=255)

    @validator('password')
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Mật khẩu phải chứa ít nhất một chữ số')
        if not any(char.isupper() for char in v):
            raise ValueError('Mật khẩu phải chứa ít nhất một chữ hoa')
        return v

class UserLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_info: "UserInfoResponse"

class UserInfoResponse(BaseModel):
    #account
    account_id: int
    username: str
    email: str
    password: str
    role: str
    is_active: bool

    #user_profile
    user_id: int
    name: str
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    address: Optional[str]

    created_at: datetime

    class Config:
        from_attributes = True

class PasswordChangeRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=8)

class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=10)
    address: Optional[str] = Field(None, max_length=255)