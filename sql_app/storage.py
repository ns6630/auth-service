from pydantic.networks import EmailStr
from sql_app.models import User
from typing import Protocol


class Storage(Protocol):
    def get_user_by_id(self, id: int) -> User:
        ...

    def get_user_by_email(self, email: EmailStr) -> User:
        ...

    def delete_user_by_id(self, id: int) -> None:
        ...

    def add_user(self, user: User) -> User:
        ...

    def update_user(self, user: User) -> User:
        ...
