import os
import json
from dotenv import load_dotenv
from datetime import datetime
from twilio.rest import Client
import requests

load_dotenv()

# Setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(account_sid, auth_token)
todoist_token = os.getenv("TODOIST_API_TOKEN")
headers = {"Authorization": f"Bearer {todoist_token}"}

# Load previous alert log
LOG_FILE = "nudge_log.json"
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        sent_ids = set(json.load(f))
else:
    sent_ids = set()

# Check today + overdue tasks
filters = ["today", "overdue"]
new_high_priority = []

for f in filters:
    response = requests.get(
        "https://api.todoist.com/rest/v2/tasks",
        headers=headers,
        params={"filter": f}
    )
    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            if task.get("priority") == 4 and task["id"] not in sent_ids:
                new_high_priority.append(task)

# Send SMS and update log
if new_high_priority:
    task_list = "\n".join([f"- {task['content']}" for task in new_high_priority])
    message_body = (
        f"🚨 Priority Alert from Willow:\n"
        f"You've got high-priority tasks due:\n{task_list}\n"
        f"Let's knock these out while they’re fresh!"
    )

    message = twilio_client.messages.create(
        body=message_body,
        from_="+16137043815",
        to="+16133719889"
    )

    # Update log
    sent_ids.update(task["id"] for task in new_high_priority)
    with open(LOG_FILE, "w") as f:
        json.dump(list(sent_ids), f)

    print("Nudge sent!")
else:
    print("No new high-priority tasks.")
