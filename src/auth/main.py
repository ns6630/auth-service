from pydantic.networks import EmailStr
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from auth.utils.email import send_registration_code
from auth.utils.system import sqlalchemy_object_as_dict, create_registration_code, hash_password
from auth.utils.jwt_utils import get_jwt_tokens_for_user
from auth.exceptions import UserAlreadyExists
from . import schemas, crud
from .database import SessionLocal
import json

app = FastAPI()


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sign-up", response_model=schemas.UserOut)
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = crud.create_user(db, user=user)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=400, detail="Указанный Email уже используется")

    registration_code = schemas.RegistrationCodeBase(
        code=create_registration_code(),
        user_id=db_user.id
    )
    db_registration_code = crud.create_registration_code(
        db, registration_code=registration_code)
    send_registration_code(email=db_user.email, code=db_registration_code.code)
    return db_user


@app.post("/sign-in")
def sign_in(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    is_valid_user_exist(db_user)
    if db_user.password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Неверный пароль")

    response_user = schemas.UserOut(**sqlalchemy_object_as_dict(db_user))
    response = get_jwt_tokens_for_user(response_user)

    refresh_token_schema = schemas.RefreshTokenBase(
        token=response["refresh_token"], user_id=db_user.id)
    crud.create_refresh_token(db, refresh_token=refresh_token_schema)
    return json.dumps(response)


@app.post("/sign-out")
def sign_out(access_token: str):
    pass


@app.post("/change-password", status_code=200)
def change_password(user_id: int, old_password: str, new_password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    is_valid_user_exist(db_user)
    if db_user.password != hash_password(old_password):
        raise HTTPException(status_code=400, detail="Неверный пароль")
    crud.update_user_password(db, user_id=user_id, new_password=hash_password(new_password))
    crud.delete_refresh_tokens_by_user_id(db, user_id=user_id)
    return json.dumps({"message": "Пароль был обновлен"})


async def send_email_code(email: EmailStr):
    pass


async def confirm_email():
    pass


def is_valid_user_exist(db_user):
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not db_user.confirmed:
        raise HTTPException(
            status_code=403, detail="Пользователь не завершил регистрацию")
