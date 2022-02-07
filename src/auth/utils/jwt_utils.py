import jwt
import datetime
from auth import schemas
from auth.configuration import JWT_PRIVATE_KEY, ACCESS_TOKEN_EXP, REFRESH_TOKEN_EXP


def get_jwt_tokens_for_user(user: schemas.UserOut):
    datetime_now = datetime.datetime.utcnow()

    access_token_dict = {
        **user.dict(),
        "exp": datetime_now + datetime.timedelta(minutes=ACCESS_TOKEN_EXP)
    }
    access_token = jwt.encode(payload=access_token_dict, key=JWT_PRIVATE_KEY, algorithm="RS256")

    refresh_token_dict = {
        "id": user.id,
        "exp": datetime_now + datetime.timedelta(days=REFRESH_TOKEN_EXP)
    }
    refresh_token = jwt.encode(payload=refresh_token_dict, key=JWT_PRIVATE_KEY, algorithm="RS256")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
