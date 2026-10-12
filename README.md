# Task Management API

A RESTful API for managing tasks, built with Python and Flask. It supports full CRUD operations, input validation, a SQL database, automated tests, and is deployed to production on Render.

**Live API:** https://task-manager-api-rq0k.onrender.com

> Note: this runs on a free hosting tier. The first request after a quiet period can take 30-60 seconds to wake the server, and stored tasks may reset when the service restarts or redeploys.

## Tech Stack

- Python 3, Flask
- Flask-SQLAlchemy (ORM) with SQLite
- Pytest for automated tests
- Gunicorn as the production server
- Deployed on Render

## Endpoints

| Method | Route | Description | Success |
|--------|-------|-------------|---------|
| GET | `/` | Lists the available endpoints | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/<id>` | Get one task by id | 200 |
| POST | `/tasks` | Create a task (JSON body with `title`) | 201 |
| PATCH | `/tasks/<id>` | Update a task (JSON body with `title` and/or `done`) | 200 |
| DELETE | `/tasks/<id>` | Delete a task | 200 |

Errors return JSON, for example `{"error": "Task not found"}`, with a `400` for invalid input or a `404` when a task doesn't exist.

### Example requests

```bash
# Create a task
curl -X POST https://task-manager-api-rq0k.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write my README"}'

# Mark task 1 as done
curl -X PATCH https://task-manager-api-rq0k.onrender.com/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'
```

## Run Locally

```bash
git clone https://github.com/Esther9904/task-manager-api.git
cd task-manager-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

The API runs at `http://127.0.0.1:5000`. The database and its tables are created automatically on first start.

## Run Tests

```bash
pytest
```

The tests use a separate in-memory database, so they never touch real data.

## Project Structure

```
app.py          # app factory: creates and configures the Flask app
extensions.py   # shared database object
models.py       # Task model
routes.py       # endpoints, grouped as a Blueprint
test_app.py     # pytest test suite
```