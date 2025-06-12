import os
import smtplib
import ssl
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime
from get_todoist_tasks import get_tasks  # Import your task-fetching function

load_dotenv()

smtp_host = os.getenv("SMTP_HOST")
smtp_port = int(os.getenv("SMTP_PORT"))
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")

PROFILE_PICTURE_URL = "https://i.imgur.com/3L3yENx.png"

themes = [
    "🌟 Motivation Monday",
    "🧠 Tactical Tuesday",
    "🌿 Wellness Wednesday",
    "⚡️ Thrive Thursday",
    "🎯 Focus Friday",
    "☀️ Set-up Saturday",
    "🧘‍♀️ Self-care Sunday"
]

greetings = [
    "Once, a guy named Sam had a mountain of tasks and no idea where to begin. He picked one tiny thing—responding to an email—and did it. That small start gave him momentum. Moral? Progress isn’t about perfection—it’s about starting.",
    "They say strategy beats hustle. Today, take a minute to plan, and watch how everything flows smoother. Even one clear priority can change the whole day.",
    "There was once a coffee shop owner who, every morning, left notes of encouragement for strangers. One customer later said it changed his week. You never know the power of small actions.",
    "Think of your productivity like a battery. A full charge doesn’t come from stress—it comes from progress. One thing at a time. Let’s thrive today.",
    "Imagine your goals as a dartboard and your tasks as darts. Focus, aim, throw. Today’s about hitting small targets to stay sharp.",
    "Saturday’s your backstage day: prep, polish, realign. What you do today sets the tone for next week—light work, big payoff.",
    "Self-care isn’t laziness—it’s productivity fuel. If you're recharging today, you're still working on your goals. Be kind to yourself."
]

goodbyes = [
    "Let’s set the tone for the week. You've got this.",
    "Think smart, act steady—today’s in your hands.",
    "Take care of yourself as much as your tasks. Balance is the goal.",
    "Energy flows where focus goes. Let’s make it count!",
    "A little intention makes a big difference. You're ready.",
    "Set it up, line it up—next week’s success starts now.",
    "Breathe, stretch, reflect. Monday will thank you."
]

# Use weekday index to select messages
index = datetime.now().weekday()
theme = themes[index]
daily_greeting = greetings[index]
daily_goodbye = goodbyes[index]

# Fetch tasks
tasks_data = get_tasks()

tasks_html = (
    ''.join(
        f"<li style='margin-bottom: 8px;'>{task['content']} "
        f"<span style='color: #999; font-size: 12px;'>({task['due']['date']})</span></li>"
        if task.get('due') else f"<li style='margin-bottom: 8px;'>{task['content']}</li>"
        for task in tasks_data
    )
    if tasks_data else "<li>🎉 No tasks today. Enjoy your free time!</li>"
)

# Build HTML email
email_body = f"""
<html>
  <body style="margin:0; padding:0; font-family: 'Segoe UI', sans-serif; background-color: #f4f6f9; color: #333;">
    <div style="max-width: 600px; margin: 30px auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
      <div style="padding: 25px 20px; text-align: center; background-color: #e3f2fd;">
        <img src="{PROFILE_PICTURE_URL}" alt="Willow" style="width: 80px; height: 80px; border-radius: 50%; margin-bottom: 15px;">
        <h1 style="margin: 5px 0; color: #0077cc;">{theme}</h1>
        <p style="font-size: 16px; max-width: 500px; margin: 10px auto;">{daily_greeting}</p>
      </div>
      <div style="padding: 20px;">
        <h3 style="margin-top: 0; color: #333;">Today's tasks — {datetime.now().strftime('%A, %B %d')}:</h3>
        <ul style="padding-left: 20px; font-size: 16px; line-height: 1.6; margin-top: 10px;">
          {tasks_html}
        </ul>
      </div>
      <div style="padding: 20px; text-align: center; background-color: #f1f3f5;">
        <p style="margin: 0; font-style: italic; color: #555;">{daily_goodbye}</p>
      </div>
    </div>
  </body>
</html>
"""

# Send the email
msg = MIMEMultipart('alternative')
msg['Subject'] = f"{theme} – Your Daily Task Reminder from Willow"
msg['From'] = "dev@ottawaserver.com"
msg['To'] = "bazinet@movie-list.com"
msg.attach(MIMEText(email_body, 'html'))

context = ssl.create_default_context()
with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.starttls(context=context)
    server.login(email_user, email_pass)
    server.send_message(msg)

print("Email sent successfully!")
