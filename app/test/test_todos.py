from ..routers.todos import get_db
from ..utils.auth_dependency import get_current_user
from ..models import Todos
from .utils import *
from ..main import app

# Applying overrides
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


# checks if an authenticated user can read all todos
def test_read_all_authenticated(test_client, test_todo):
    response = test_client.get("/todos")
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


def test_read_todo_authenticated(test_client, test_todo):
    response = test_client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "complete": False,
        "title": "Learn to test",
        "description": "Need to learn pytest",
        "priority": 5,
        "owner_id": 1,
    }


def test_read_not_found_todo(test_client, test_todo):
    response = test_client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_created_todo_item(test_client, test_todo, test_db):
    request_data = {
        "title": "New todo",
        "description": "new todo description",
        "priority": 5,
        "complete": False,
    }

    response = test_client.post("/todos/create_todo", json=request_data)
    assert response.status_code == 201

    todo_model = test_db.query(Todos).filter(Todos.id == 2).first()

    assert todo_model.title == request_data.get("title")
    assert todo_model.description == request_data.get("description")
    assert todo_model.priority == request_data.get("priority")
    assert todo_model.complete == request_data.get("complete")


def test_updated_todo(test_client, test_todo, test_db):
    request_data = {
        "title": "updated todo",
        "description": "update todo description",
        "priority": 6,
        "complete": False,
    }

    response = test_client.put("/todos/1", json=request_data)
    assert response.status_code == 204

    todo_model = test_db.query(Todos).filter(Todos.id == 1).first()

    assert todo_model.title == "updated todo"
    assert todo_model.description == "update todo description"
    assert todo_model.priority == 6


def test_updating_not_found_todo(test_client, test_todo):
    request_data = {
        "title": "updated todo",
        "description": "update todo description",
        "priority": 6,
        "complete": False,
    }

    response = test_client.put("/todos/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_deleted_todo(test_client, test_todo, test_db):
    response = test_client.delete("/todos/1")
    assert response.status_code == 204
    todo_model = test_db.query(Todos).filter(Todos.id == 1).first()
    assert todo_model is None
