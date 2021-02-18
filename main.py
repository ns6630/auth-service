import sqlalchemy
import databases

from pydantic.networks import EmailStr
from sql_app.models import User, UserIn
from fastapi import FastAPI


DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

UserTable = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("middle_name", sqlalchemy.String),
    sqlalchemy.Column("last_name", sqlalchemy.String),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("refresh_token", sqlalchemy.String),
    sqlalchemy.Column("confirmed", sqlalchemy.Boolean),
    sqlalchemy.Column("registration_date", sqlalchemy.DateTime),    
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sign-up")
async def sign_up(user: UserIn):
    query = UserTable.insert().values(email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


async def sign_in(user: UserIn):
    return {
        'auth_token': 'auth_token_str',
        'access_token': 'access_token_str'
    }


async def sign_out(auth_token: str):
    pass


async def send_email_code(email: EmailStr):
    pass


async def confirm_email():
    pass
