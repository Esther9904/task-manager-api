from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build Task API", "done": False}
]


def find_max(tasks):
    maximum = []
    if len(tasks) == 0:
        raise ValueError("No tasks available")
        return
    for task in tasks:
        maximum.append(task["id"])
    result = max(maximum) + 1
    return result


@app.route("/")
def home():
    return "Hello, Task Manager!"

@app.route("/tasks")
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks/<int:task_id>")
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    next_id = find_max(tasks)
    new_task = {"id": next_id, "title": data["title"], "done": False}
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            if "title" in data:
                task["title"] = data["title"]
            if "done" in data: 
                task["done"] = data["done"]
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"})
    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)