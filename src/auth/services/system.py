import hashlib
from auth.settings import SALT
from uuid import uuid4

def salt_password(password: str):
    return SALT + password

def hash_password(password: str):
    salted_password = salt_password(password)
    return hashlib.sha256(salted_password.encode("utf-8")).hexdigest()

def password_is_valid(password: str):
    # Функция для валидации нового сырого пароля.
    return True

def create_registration_code():
    return str(uuid4())