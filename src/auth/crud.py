from auth.utils.core import hash_password
from sqlalchemy.orm import Session
from auth import schemas, models
from sqlalchemy.exc import IntegrityError
from auth.exceptions import UserAlreadyExists


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
    )
    db.add(db_user)

    try:
        db.commit()
    except IntegrityError:
        raise UserAlreadyExists()

    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate):
    db.query(models.User).filter(
        models.User.id == user.id).update(user.dict())
    db.commit()
    return db.query(models.User).filter(models.User.id == user.id).first()


def delete_user(db: Session, user_id: int):
    delete_count = db.query(models.User).filter(
        models.User == user_id).delete()
    db.commit()
    return delete_count


def get_registration_code(db: Session, user_id: int):
    return db.query(models.RegistrationCode).filter(models.RegistrationCode.user_id == user_id).first()


def create_registration_code(db: Session, registration_code: schemas.RegistrationCodeBase):
    db_registration_code = models.RegistrationCode(**registration_code.dict())
    db.add(db_registration_code)
    db.commit()
    db.refresh(db_registration_code)
    return db_registration_code


def delete_registration_code(db: Session, user_id: int):
    delete_count = db.query(models.RegistrationCode).filter(
        models.RegistrationCode.user_id == user_id).delete()
    db.commit()
    return delete_count


def get_refresh_token(db: Session, token: str):
    return db.query(models.RefreshToken).filter(models.RefreshToken.token == token).first()


def create_refresh_token(db: Session, refresh_token: schemas.RefreshTokenBase):
    db_refresh_token = models.RefreshToken(**refresh_token.dict())
    db.add(db_refresh_token)
    db.commit()
    db.refresh(db_refresh_token)
    return db_refresh_token


def delete_refresh_token(db: Session, token: str):
    delete_count = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == token).delete()
    db.commit()
    return delete_count


def delete_refresh_tokens_by_user_id(db: Session, user_id: int):
    delete_count = db.query(models.RefreshToken).filter(
        models.RefreshToken.user_id == user_id).delete()
    db.commit()
    return delete_count


def confirm_user(db: Session, user_id: int):
    db.query(models.User).filter(
        models.User.id == user_id).update({"confirmed": True})
    db.commit()
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user_password(db: Session, user_id: int, new_password: str):
    db.query(models.User).filter(
        models.User.id == user_id).update({"password": new_password})
    db.commit()
    return db.query(models.User).filter(models.User.id == user_id).first()
