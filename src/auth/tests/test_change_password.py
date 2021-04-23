import json
from auth.crud import confirm_user
from auth.main import sign_up, change_password
from auth import schemas


def test_change_password(db):
    user = schemas.UserCreate(
        email="test@test.test",
        password="testpassword"
    )
    db_user = sign_up(user=user, db=db)
    db_user = confirm_user(db=db, user_id=db_user.id)

    password = "newpassword"
    response = json.loads(
        change_password(user_id=db_user.id, old_password=user.password, new_password=password, db=db))
    assert response["message"] == "Пароль был обновлен"
