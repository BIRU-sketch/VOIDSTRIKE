import os
from dotenv import load_dotenv

load_dotenv()

name = "Goblin"
model = "gemini-3.1-flash-lite"
api_key = os.getenv("GEMINI_API_KEY")

window_size ="520x720"
min_window_size = (420, 520)

system_prompt=f"""
You are a helpfull desktop automation AI assistant serving as the orchestrator for a tool.
Execute the tasks you are given and be very concise when you explain.
"""