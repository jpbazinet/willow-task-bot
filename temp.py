import requests

url = "https://replit.com/@bazinet/willow-task-bot?v=1/add-task"

payload = {
    "content": "Test2 from Willow",
    "due": "today at 2pm",
    "priority": 4
}

resp = requests.post(url, json=payload)
print("Status:", resp.status_code)
print("Response:", resp.json())
