import pytest
from fastapi import HTTPException

from auth import schemas
from auth.main import sign_up


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
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )
    sign_up(user=user, db=db)

    with pytest.raises(HTTPException) as exc:
        sign_up(user=user, db=db)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Указанный Email уже используется"
