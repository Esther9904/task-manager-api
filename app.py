from flask import Flask, jsonify

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build Task API", "done": False}
]

@app.route("/")
def home():
    return "Hello, Task Manager!"

@app.route("/tasks")
def get_tasks():
    return jsonify(tasks)

if __name__ == "__main__":
    app.run(debug=True)