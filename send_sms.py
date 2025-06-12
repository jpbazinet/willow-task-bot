import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import datetime
from get_todoist_tasks import get_tasks  # Shared task-fetching

load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

# Day-based intro themes
intros = [
    "🌟 Motivation Monday 💪",
    "🧠 Tactical Tuesday 🔧",
    "🌿 Wellness Wednesday 💚",
    "⚡ Thrive Thursday ⚡",
    "🎯 Focus Friday 🎯",
    "☀️ Set-up Saturday 🛠️",
    "🧘‍♀️ Self-care Sunday 😌"
]

quotes = [
    "Start small, finish strong.",
    "Slow progress is still progress.",
    "You’re one task away from momentum.",
    "Eat the frog 🐸: do the hardest task first.",
    "No zero days. Just do something.",
    "Tasks don't stand a chance against you.",
    "You're not busy—you're building something."
]

# Determine the day
index = datetime.now().weekday()
intro = intros[index]
quote = quotes[index]

# Get tasks
tasks_data = get_tasks()

# Format SMS content
if tasks_data:
    task_list = "\n".join([f"- {task['content']}" for task in tasks_data])
    message_body = f"{intro}\n📝 Willow here:\n{task_list}\n\n💬 {quote}"
else:
    message_body = f"{intro}\n🎉 No tasks today! Recharge & shine bright.\n💬 {quote}"

# Send SMS
message = client.messages.create(
    body=message_body,
    from_="+16137043815",
    to="+16133719889"
)

print("SMS sent!")
