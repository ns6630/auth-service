from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    id: int
    first_name: Optional[str] = ""
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""
    full_name: Optional[str] = ""

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserUpdate(UserCreate):
    id: int
    first_name: Optional[str] = ""
    middle_name: Optional[str] = ""
    last_name: Optional[str] = ""
    full_name: Optional[str] = ""


class User(UserUpdate):
    refresh_token: str
    confirmed: bool
    registration_date: datetime

    class Config:
        orm_mode = True


class RegistrationCodeBase(BaseModel):
    code: str


class RegistrationCode(RegistrationCodeBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True