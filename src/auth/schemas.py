from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    first_name: Optional[str] = ""
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""
    full_name: Optional[str] = ""

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    id: int
    first_name: Optional[str] = ""
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""
    full_name: Optional[str] = ""

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    first_name: Optional[str] = ""
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""
    full_name: Optional[str] = ""
    confirmed: bool
    registration_date: datetime

    class Config:
        orm_mode = True


class RefreshTokenBase(BaseModel):
    token: str
    user_id: int


class RefreshToken(RefreshTokenBase):
    id: int

    class Config:
        orm_mode = True


class SignInResponse(BaseModel):
    access_token: str
    refresh_token: str


class ChangePasswordResponse(BaseModel):
    message: str


class RegistrationCodeBase(BaseModel):
    code: str
    user_id: int


class RegistrationCode(RegistrationCodeBase):
    id: int

    class Config:
        orm_mode = True
