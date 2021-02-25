from pathlib import Path
import os


SALT = os.getenv("AUTH_SALT", "example_salt")

jwt_private_key_path = Path(os.getenv("AUTH_JWT_PRIVATE_KEY_PATH", "auth/configuration/rsa_keys/test"))
with open(jwt_private_key_path, "rb") as f:
    JWT_PRIVATE_KEY = f.read()

jwt_public_key_path = Path(os.getenv("AUTH_JWT_PUBLIC_KEY_PATH", "auth/configuration/rsa_keys/test.pub"))
with open(jwt_public_key_path, "rb") as f:
    JWT_PUBLIC_KEY = f.read()

# minutes
ACCESS_TOKEN_EXP = int(os.getenv("AUTH_ACCESS_TOKEN_EXP", "15"))

# days
REFRESH_TOKEN_EXP = int(os.getenv("AUTH_REFRESH_TOKEN_EXP", "30"))
