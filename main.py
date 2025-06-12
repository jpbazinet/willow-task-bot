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


import base64

@app.route('/update-github-file', methods=['POST'])
def update_github_file():
    data = request.json
    filename = data.get("filename")
    new_content = data.get("new_content")
    commit_message = data.get("commit_message", "Update file via Willow")

    github_token = os.getenv("GITHUB_TOKEN")
    repo = "bazinet/willow-task-bot"
    branch = "main"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }

    # Step 1: Get the file SHA
    get_url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    get_params = {"ref": branch}
    get_resp = requests.get(get_url, headers=headers, params=get_params)

    if get_resp.status_code != 200:
        return {"error": f"Could not retrieve file: {get_resp.text}"}, 400

    sha = get_resp.json().get("sha")

    # Step 2: Update file content
    content_encoded = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    update_data = {
        "message": commit_message,
        "content": content_encoded,
        "sha": sha,
        "branch": branch,
        "committer": {
            "name": "Willow",
            "email": "willow@assistant.ai"
        }
    }

    update_resp = requests.put(get_url, headers=headers, json=update_data)
    if update_resp.status_code not in [200, 201]:
        return {"error": f"Failed to update file: {update_resp.text}"}, 400

    return {"message": "File updated successfully", "commit": update_resp.json().get("commit")}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
