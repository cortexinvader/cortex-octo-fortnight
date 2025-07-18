import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# Database file location
SQLITE_DB = "data/ai_system.db"
