import hashlib
from auth.configuration import SALT
from uuid import uuid4
from sqlalchemy import inspect


def hash_password(password: str):
    def salt_password(raw_password: str):
        return SALT + raw_password

    salted_password = salt_password(password)
    return hashlib.sha256(salted_password.encode("utf-8")).hexdigest()


def password_is_valid(password: str):
    # Функция для валидации нового сырого пароля.
    return True


def create_registration_code():
    return str(uuid4())


def sqlalchemy_object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
