import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("TODOIST_API_TOKEN")

headers = {
    "Authorization": f"Bearer {token}"
}

def get_tasks():
    """Fetches both today's and overdue tasks from Todoist."""
    try:
        today_response = requests.get(
            "https://api.todoist.com/rest/v2/tasks",
            headers=headers,
            params={"filter": "today"}
        )
        overdue_response = requests.get(
            "https://api.todoist.com/rest/v2/tasks",
            headers=headers,
            params={"filter": "overdue"}
        )

        today_tasks = today_response.json() if today_response.status_code == 200 else []
        overdue_tasks = overdue_response.json() if overdue_response.status_code == 200 else []

        return overdue_tasks + today_tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return []
