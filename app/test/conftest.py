import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from ..models import Todos, Users
from ..main import app
from .utils import TestingSessionLocal, engine
from ..utils.passwordhash import get_hash_password

client = TestClient(app)


@pytest.fixture
def test_todo():
    # initialise newtodo
    todo = Todos(
        title="Learn to test",
        description="Need to learn pytest",
        priority=5,
        complete=False,
        owner_id=1,
    )
    # save newtodo in test db
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        # delete newtodo to cleanup
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="dennisappiah",
        email="appiahdennis@gmail.com",
        firstname="dennis",
        lastname="appiah",
        hashed_password=get_hash_password("testpassword"),
        role="admin",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


@pytest.fixture
def test_client():
    yield client


@pytest.fixture
def test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
