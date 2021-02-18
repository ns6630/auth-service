from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from sqlalchemy.sql.operators import comma_op
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "fake_salt"
    db_user = models.User(
        email=user.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session, user: schemas.UserUpdate):
    hashed_password = user.password + "fake_salt"
    db.query(models.User).filter(models.User.id == user.id).update(**user.dict())
    

def create_registration_code(db: Session, code: schemas.RegistrationCodeBase, user_id: int):
    db_registration_code = models.RegistrationCode(
        **code.dict(),
        user_id=user_id
    )
    db.add(db_registration_code)
    db.commit()
    db.refresh(db_registration_code)
    return db_registration_code

def delite_registration_code(db:Session, user_id: int):
    pass
