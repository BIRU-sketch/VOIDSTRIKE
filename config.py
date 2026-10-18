import os
from dotenv import load_dotenv

load_dotenv()

name = "Goblin"
model = "gemini-3.8-flash"
api_key = os.getenv("GEMINI_API_KEY")

window_size ="520x720"
min_window_size = (420, 520)

system_prompt = f"""
You are a friendly and concise AI assistant .
Keeep your responses short and helpful.
"""