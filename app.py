from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select


db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return{"id": self.id, "title": self.title, "done": self.done}


def create_app(database_uri="sqlite:///tasks.db"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    db.init_app(app)

    @app.route("/")
    def home():
        return "Hello, Task Manager!"

    @app.route("/tasks")
    def get_tasks():
        all_tasks = db.session.execute(select(Task)).scalars().all()
        return jsonify([task.to_dict() for task in all_tasks])

    @app.route("/tasks/<int:task_id>")
    def get_task(task_id):
        one_task = db.session.get(Task, task_id)
        if one_task:
            return jsonify(one_task.to_dict())
        return jsonify({"error": "Task not found"}), 404

    @app.route("/tasks", methods=["POST"])
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

    @app.route("/tasks/<int:task_id>", methods=["PATCH"])
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

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        task = db.session.get(Task, task_id)
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"})

    return app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)