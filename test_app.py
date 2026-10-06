import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app(database_uri="sqlite:///:memory:")
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Real Task"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "title": "Real Task", "done": False}

def test_create_task_missing_title(client):
    response = client.post("/tasks", json={"color": "red"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Title is required"}

def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}
    