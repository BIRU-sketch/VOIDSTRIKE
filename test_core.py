from core.gemini_client import GeminiClient

bot = GeminiClient()
print(bot.send('hello which model am i talking to right now? '))