import time
import datetime

def execute(query=None):
    now = time.localtime()
    formatted_time = time.strftime("%I:%M %p", now)       # e.g., 02:15 PM
    formatted_date = time.strftime("%A, %B %d, %Y", now)   # e.g., Friday, July 18, 2025

    return (
        f"🧠 Hi there! Just letting you know that this is the bot's system time:\n\n"
        f"📅 Date: {formatted_date}\n"
        f"⏰ Time: {formatted_time}"
    )
