from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    confirmed = Column(Boolean, default=False)
    registration_date = Column(DateTime, default=datetime.now)

    registration_code = relationship(
        "RegistrationCode", uselist=False, back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    token = Column(String, index=True)

    user = relationship("User", back_populates="refresh_tokens")


class RegistrationCode(Base):
    __tablename__ = "registration_code"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete="CASCADE"), unique=True)
    code = Column(String)

    user = relationship("User", back_populates="registration_code")
