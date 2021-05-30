import jwt
from pydantic.networks import EmailStr
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from auth.utils.email import send_registration_code
from auth.utils.system import sqlalchemy_object_as_dict, create_registration_code, hash_password
from auth.utils.jwt_utils import get_jwt_tokens_for_user
from auth.exceptions import UserAlreadyExists
from . import schemas, crud
from .configuration import JWT_PUBLIC_KEY
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


@app.post("/sign-in", response_model=schemas.SignInResponse)
def sign_in(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    raise_if_user_not_valid(db_user)
    if db_user.password != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Неверный пароль")

    return get_jwt_tokens(db, db_user)


@app.post("/refresh-tokens", response_model=schemas.SignInResponse)
def refresh_tokens(refresh_token: str, db: Session = Depends(get_db)):
    try:
        refresh_token_decoded = jwt.decode(jwt=refresh_token, key=JWT_PUBLIC_KEY, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истек")
    db_user = crud.get_user(db, user_id=refresh_token_decoded["id"])
    raise_if_user_not_valid(db_user)
    crud.delete_refresh_token(db, token=refresh_token)
    response = get_jwt_tokens(db, db_user)
    return response


@app.post("/sign-out")
def sign_out(access_token: str):
    pass


@app.post("/change-password", response_model=schemas.ChangePasswordResponse)
def change_password(user_id: int, old_password: str, new_password: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    raise_if_user_not_valid(db_user)
    if db_user.password != hash_password(old_password):
        raise HTTPException(status_code=400, detail="Неверный пароль")
    crud.update_user_password(db, user_id=user_id, new_password=hash_password(new_password))
    crud.delete_refresh_tokens_by_user_id(db, user_id=user_id)
    return json.dumps({"message": "Пароль был обновлен"})


async def send_email_code(email: EmailStr):
    pass


async def confirm_email():
    pass


def raise_if_user_not_valid(db_user):
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if not db_user.confirmed:
        raise HTTPException(
            status_code=403, detail="Пользователь не завершил регистрацию")


def get_jwt_tokens(db, db_user):
    user = schemas.UserOut(**sqlalchemy_object_as_dict(db_user))
    response = get_jwt_tokens_for_user(user)
    refresh_token = schemas.RefreshTokenBase(
        token=response["refresh_token"], user_id=db_user.id)
    crud.create_refresh_token(db, refresh_token=refresh_token)
    return json.dumps(response)
