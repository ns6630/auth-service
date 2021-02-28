from pydantic.networks import EmailStr
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from auth.services.email import send_registration_code
from auth.services.system import create_registration_code
from auth.sql_app.exceptions import UserAlreadyExists

from . import crud, models, schemas
from .database import SessionLocal, engine


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


# @app.post("/sign-in")
# async def sign_in(user: UserIn):
#     return {
#         'auth_token': 'auth_token_str',
#         'access_token': 'access_token_str'
#     }


async def sign_out(auth_token: str):
    pass


async def send_email_code(email: EmailStr):
    pass


async def confirm_email():
    pass
