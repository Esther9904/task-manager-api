from flask import Blueprint, jsonify, request
from sqlalchemy import select
from extensions import db
from models import Task

bp = Blueprint("tasks", __name__)

@bp.route("/")
def home():
    return jsonify(
        {
            "message": "Hello Task Manager",
            "endpoints": {
                "GET /tasks": "List all tasks",
                "GET /tasks/<id>": "Get a single task by id",
                "POST /tasks": "Make a new task -(JSON body is expected)",
                "PATCH /tasks/<id>": "Update a specific task - (JSON body is expected)",
                "DELETE /tasks/<id>": "Delete a specific task"

            }
            
        }
    )

@bp.route("/tasks")
def get_tasks():
    all_tasks = db.session.execute(select(Task)).scalars().all()
    return jsonify([task.to_dict() for task in all_tasks])

@bp.route("/tasks/<int:task_id>")
def get_task(task_id):
    one_task = db.session.get(Task, task_id)
    if one_task:
        return jsonify(one_task.to_dict())
    return jsonify({"error": "Task not found"}), 404

@bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty body"}), 400
    if "title" not in data or not data["title"].strip():
        return jsonify({"error": "Title is required"}), 400
    new_task = Task(title=data["title"])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@bp.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Empty body"}), 400
    if "title" not in data and "done" not in data:
        return jsonify({"error": "Nothing to update"}), 400
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    if "title" in data:
        task.title = data["title"]
    if "done" in data:
        task.done = data["done"]
    
    db.session.commit()
    return jsonify(task.to_dict())

@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
