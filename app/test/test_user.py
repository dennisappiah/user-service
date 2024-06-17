from ..routers.todos import get_db
from ..utils.auth_dependency import get_current_user
from .utils import *
from ..main import app


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_return_user(test_client, test_user):
    response = test_client.get("/user")
    assert response.status_code == 200
    assert response.json()["username"] == "dennisappiah"
    assert response.json()["email"] == "appiahdennis@gmail.com"
    assert response.json()["firstname"] == "dennis"


def test_user_change_password_success(test_client, test_user):
    request_data = {
        "password": "testpassword",
        "new_password": "testpassword2",
    }
    response = test_client.put("/user/password", json=request_data)
    assert response.status_code == 204


def test_user_change_password_invalid(test_client, test_user):
    request_data = {
        "password": "wrong_password",
        "new_password": "testpassword2",
    }
    response = test_client.put("/user/password", json=request_data)
    assert response.status_code == 401
    assert response.json() == {"detail": "Error on password change"}
