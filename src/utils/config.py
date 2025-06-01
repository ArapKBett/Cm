import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
    DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
    LOG_FILE = "logs/bot.log"
    CHART_DIR = "charts"
    DATA_REFRESH_INTERVAL = 3600  # Refresh data every hour
