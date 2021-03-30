import json
from auth.crud import confirm_user, get_refresh_token
from auth.main import sign_in, sign_up, change_password, refresh_tokens
from auth import schemas
import pytest
from fastapi import HTTPException
import time


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


def test_sign_in(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )

    with pytest.raises(HTTPException) as exc:
        sign_in(user=user, db=db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Пользователь не найден"

    db_user = sign_up(user=user, db=db)
    with pytest.raises(HTTPException) as exc:
        sign_in(user=user, db=db)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Пользователь не завершил регистрацию"

    user_wrong_password = schemas.UserCreate(
        email="test@test.test",
        password="wrongpassword"
    )

    db_user = confirm_user(db=db, user_id=db_user.id)
    with pytest.raises(HTTPException) as exc:
        sign_in(user=user_wrong_password, db=db)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Неверный пароль"

    response = json.loads(sign_in(user=user, db=db))
    refresh_token = response["refresh_token"]
    db_refresh_token = get_refresh_token(db, token=refresh_token)
    assert db_refresh_token.token == refresh_token


def test_change_password(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )
    db_user = sign_up(user=user, db=db)
    db_user = confirm_user(db=db, user_id=db_user.id)

    response = json.loads(sign_in(user=user, db=db))
    refresh_token = response["refresh_token"]

    password = "newpassword"
    response = json.loads(
        change_password(user_id=db_user.id, old_password="testpassword", new_password=password, db=db))
    assert response["message"] == "Пароль был обновлен"

    db_refresh_token = get_refresh_token(db, token=refresh_token)
    assert db_refresh_token is None

    user.password = password
    response = json.loads(sign_in(user=user, db=db))
    refresh_token = response["refresh_token"]
    db_refresh_token = get_refresh_token(db, token=refresh_token)
    assert db_refresh_token.token == refresh_token


def test_refresh_tokens(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )
    db_user = sign_up(user, db)
    db_user = confirm_user(db, user_id=db_user.id)
    tokens = json.loads(sign_in(user, db))
    # Для получения токена отличного от предыдущего
    time.sleep(1)
    new_tokens = json.loads(refresh_tokens(tokens["refresh_token"], db))
    refresh_token = get_refresh_token(db, tokens["refresh_token"])
    new_refresh_token = get_refresh_token(db, new_tokens["refresh_token"])

    assert refresh_token is None
    assert new_refresh_token is not None
