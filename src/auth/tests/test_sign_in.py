import json
import datetime

import pytest
from fastapi import HTTPException
from freezegun import freeze_time

from auth import schemas
from auth.configuration import REFRESH_TOKEN_EXP
from auth.crud import confirm_user
from auth.main import sign_in, sign_up, refresh_tokens, change_password


def test_sign_in_user_not_found(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )

    with pytest.raises(HTTPException) as exc:
        sign_in(user=user, db=db)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Пользователь не найден"


def test_sign_in_rejects_unconfirmed_user(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )

    sign_up(user=user, db=db)
    with pytest.raises(HTTPException) as exc:
        sign_in(user=user, db=db)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Пользователь не завершил регистрацию"


def test_sign_in_rejects_wrong_password(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )

    db_user = sign_up(user=user, db=db)
    confirm_user(db=db, user_id=db_user.id)

    user_wrong_password = schemas.UserCreate(
        email="test@test.test",
        password="wrongpassword"
    )

    with pytest.raises(HTTPException) as exc:
        sign_in(user=user_wrong_password, db=db)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Неверный пароль"


def test_sign_in_with_refresh_token(db):
    # Мокаем время.
    now = datetime.datetime(2021, 1, 1)

    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )
    with freeze_time(now):
        db_user = sign_up(user, db)
    confirm_user(db, user_id=db_user.id)
    tokens = json.loads(sign_in(user, db))

    # "Ждем" пять минут для получения токена отличного от предыдущего.
    now = now + datetime.timedelta(minutes=5)
    with freeze_time(now):
        new_tokens = json.loads(refresh_tokens(tokens["refresh_token"], db))

    assert new_tokens is not None


def test_sign_in_rejects_invalid_refresh_token(db):
    # Мокаем время.
    now = datetime.datetime(2021, 1, 1)

    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )

    db_user = sign_up(user, db)
    confirm_user(db, user_id=db_user.id)
    with freeze_time(now):
        tokens = json.loads(sign_in(user, db))

    # "Ждем" пока refresh_token "протухнет".
    now = now + datetime.timedelta(days=REFRESH_TOKEN_EXP + 1)

    with freeze_time(now):
        with pytest.raises(HTTPException) as exc:
            refresh_tokens(tokens["refresh_token"], db)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Срок действия токена истек"


def test_sing_in_with_new_password(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )
    db_user = sign_up(user=user, db=db)
    db_user = confirm_user(db=db, user_id=db_user.id)

    password = "newpassword"
    change_password(user_id=db_user.id, old_password=user.password, new_password=password, db=db)
    user.password = password
    tokens = json.loads(sign_in(user=user, db=db))

    assert tokens is not None
