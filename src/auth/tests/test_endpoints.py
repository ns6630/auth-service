from sqlalchemy import schema
from auth.sql_app.main import get_db, sign_up
from auth.sql_app import schemas
import pytest
from fastapi import HTTPException


def test_sign_up(db):
    # arrange - подготовка

    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )

    # act - действие
    db_user = sign_up(user=user, db=db)

    # assert - проверка
    assert db_user.id is not None
    assert db_user.email == user.email


def test_sign_up_already_exists(db):
    # arrange
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )
    db_user = sign_up(user=user, db=db)

    # act
    with pytest.raises(HTTPException) as exc:
        sign_up(user=user, db=db)

    # assert
    assert exc.value.status_code == 400
    assert exc.value.detail == "Указанный Email уже используется"
