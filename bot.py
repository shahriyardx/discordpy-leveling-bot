import os
from leveling import bot
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN = os.getenv("TOKEN")

bot.run(TOKEN)
