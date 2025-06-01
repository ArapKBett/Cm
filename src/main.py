import asyncio
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
    
    # Run bots concurrently
    await asyncio.gather(
        asyncio.to_thread(telegram_bot.start),
        discord_bot.bot.start(Config.DISCORD_BOT_TOKEN)
    )

if __name__ == "__main__":
    asyncio.run(main())
