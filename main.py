from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/add-task', methods=['POST'])
def add_task():
    data = request.json
    content = data.get("content")
    due = data.get("due")  # e.g., "Thursday at 2pm"
    priority = data.get("priority", 1)

    token = os.getenv("TODOIST_API_TOKEN")
    project_id = os.getenv("WILLOW_TASKS_PROJECT_ID")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    task_data = {
        "content": content,
        "due_string": due,
        "priority": priority,
        "project_id": project_id
    }

    resp = requests.post("https://api.todoist.com/rest/v2/tasks", headers=headers, json=task_data)
    return jsonify(resp.json()), resp.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
