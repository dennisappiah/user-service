from ..routers.todos import get_db
from ..utils.auth_dependency import get_current_user
from ..models import Todos
from .utils import *
from ..main import app


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_admin_read_all_todos_by(test_client, test_todo):
    response = test_client.get("/admin/todos")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "complete": False,
            "title": "Learn to test",
            "description": "Need to learn pytest",
            "priority": 5,
            "owner_id": 1,
        }
    ]


def test_admin_delete_todo(test_client, test_todo, test_db):
    response = test_client.delete("/todos/1")
    assert response.status_code == 204

    todo_model = test_db.query(Todos).filter(Todos.id == 1).first()
    assert todo_model is None
