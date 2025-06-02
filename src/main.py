import asyncio
import sys
import os
from pathlib import Path
import signal

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.api.coinmarketcap import CoinMarketCapAPI
from src.api.forex_data import ForexData
from src.analysis.ict_analysis import ICTAnalysis
from src.analysis.prediction import Prediction
from src.visualization.chart_generator import ChartGenerator
from src.bot.telegram_bot import TelegramBot
from src.bot.discord_bot import DiscordBot
from src.utils.logger import setup_logger
from src.utils.config import Config

async def main():
    logger = setup_logger()
    logger.info("Starting Crypto ICT Bot")
    
    # Initialize components
    cmc_api = CoinMarketCapAPI()
    forex_api = ForexData()
    ict_analysis = ICTAnalysis()
    prediction = Prediction()
    chart_generator = ChartGenerator()
    
    # Initialize bots
    telegram_bot = TelegramBot(cmc_api, forex_api, ict_analysis, prediction, chart_generator)
    discord_bot = DiscordBot(cmc_api, forex_api, ict_analysis, prediction, chart_generator)
    
    # Define shutdown handler
    async def shutdown():
        logger.info("Shutting down bots...")
        await telegram_bot.application.stop()
        await telegram_bot.application.updater.stop()
        await discord_bot.bot.close()
        logger.info("Bots stopped successfully")

    # Set up signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))

    # Run bots concurrently
    try:
        await asyncio.gather(
            telegram_bot.start(),  # Directly await the async start method
            discord_bot.bot.start(Config.DISCORD_BOT_TOKEN)
        )
    except Exception as e:
        logger.error(f"Error running bots: {e}")
        await shutdown()
        raise
    finally:
        await shutdown()

if __name__ == "__main__":
    asyncio.run(main())
