from flask import Flask, request, jsonify
import os
import requests
import base64
from datetime import datetime
from dotenv import load_dotenv
from dateparser.search import search_dates

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

@app.route('/update-github-file', methods=['POST'])
def update_github_file():
    data = request.json
    filename = data.get("filename")
    new_content = data.get("new_content")
    commit_message = data.get("commit_message", "Update file via Willow")

    github_token = os.getenv("GITHUB_TOKEN")
    repo = "jpbazinet/willow-task-bot"
    branch = "main"

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    }

    get_url = f"https://api.github.com/repos/{repo}/contents/{filename}"
    get_params = {"ref": branch}
    get_resp = requests.get(get_url, headers=headers, params=get_params)

    if get_resp.status_code != 200:
        return {"error": f"Could not retrieve file: {get_resp.text}"}, 400

    sha = get_resp.json().get("sha")
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

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.json
    body = data.get("body", "🌟 Hey superstar! Willow here – everything's running smoothly.")
    from twilio.rest import Client
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    msg = client.messages.create(
        body=body,
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=os.getenv("TWILIO_RECIPIENT_NUMBER")
    )
    return {"sid": msg.sid}, 200

@app.route('/parse-task', methods=['POST'])
def parse_task():
    try:
        data = request.json
        raw_input = data.get("text")
        if not raw_input:
            return {"error": "No input provided"}, 400

        parsed_date = search_dates(raw_input)
        due = None
        content = raw_input

        if parsed_date:
            for match_text, date_obj in parsed_date:
                if date_obj and match_text.lower() in raw_input.lower():
                    due = date_obj.strftime("%A at %-I%p").lower()
                    content = raw_input.replace(match_text, "").strip()
                    break

        payload = {
            "content": content,
            "due": due or "today",
            "priority": data.get("priority", 1)
        }

        resp = requests.post("https://willow-task-bot.onrender.com/add-task", json=payload)
        return jsonify(resp.json()), resp.status_code

    except Exception as e:
        import traceback
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return {"error": "Internal server error", "details": traceback_str}, 500

@app.route('/todoist-webhook', methods=['POST'])
def todoist_webhook():
    data = request.get_json()
    print("Webhook received:", data)
    return '', 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
