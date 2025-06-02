from telegram.ext import Application, CommandHandler
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.helpers import format_date
import pandas as pd
import os
from datetime import datetime, timedelta

class TelegramBot:
    def __init__(self, cmc_api, forex_api, ict_analysis, prediction, chart_generator):
        self.cmc_api = cmc_api
        self.forex_api = forex_api
        self.ict_analysis = ict_analysis
        self.prediction = prediction
        self.chart_generator = chart_generator
        self.logger = setup_logger()
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Set up command handlers."""
        self.application.add_handler(CommandHandler("analyze", self.analyze))
        self.application.add_handler(CommandHandler("forex", self.analyze_forex))
        self.application.add_error_handler(self.error_handler)

    async def analyze(self, update, context):
        """Handle /analyze command for crypto data."""
        symbol = context.args[0].upper() if context.args else "BTC"
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        data = self.cmc_api.get_historical_data(symbol, start_date, end_date)
        if not isinstance(data, pd.DataFrame):
            await update.message.reply_text(f"Error fetching data for {symbol}.")
            return
        
        order_blocks = self.ict_analysis.find_order_blocks(data)
        market_structure = self.ict_analysis.analyze_market_structure(data)
        pred = self.prediction.predict_price(data, order_blocks, market_structure)
        
        chart_path = f"{Config.CHART_DIR}/{symbol}_chart.png"
        self.chart_generator.generate_candlestick_chart(data, symbol, order_blocks, chart_path)
        
        message = (
            f"**{symbol} Analysis**\n"
            f"Market Structure: {market_structure}\n"
            f"Prediction: {pred['direction']} to {pred['target'] or 'N/A'}\n"
            f"Order Blocks: {len(order_blocks)} found"
        )
        await context.bot.send_message(chat_id=Config.TELEGRAM_CHANNEL_ID, text=message, parse_mode="Markdown")
        await context.bot.send_photo(chat_id=Config.TELEGRAM_CHANNEL_ID, photo=open(chart_path, "rb"))

    async def analyze_forex(self, update, context):
        """Handle /forex command for forex data."""
        pair = context.args[0].upper() if context.args else "EURUSD"
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        data = self.forex_api.get_forex_data(pair, start_date, end_date)
        if not isinstance(data, pd.DataFrame):
            await update.message.reply_text(f"Error fetching forex data for {pair}.")
            return
        
        order_blocks = self.ict_analysis.find_order_blocks(data)
        market_structure = self.ict_analysis.analyze_market_structure(data)
        pred = self.prediction.predict_price(data, order_blocks, market_structure)
        
        chart_path = f"{Config.CHART_DIR}/{pair}_chart.png"
        self.chart_generator.generate_candlestick_chart(data, pair, order_blocks, chart_path)
        
        message = (
            f"**{pair} Forex Analysis**\n"
            f"Market Structure: {market_structure}\n"
            f"Prediction: {pred['direction']} to {pred['target'] or 'N/A'}\n"
            f"Order Blocks: {len(order_blocks)} found"
        )
        await context.bot.send_message(chat_id=Config.TELEGRAM_CHANNEL_ID, text=message, parse_mode="Markdown")
        await context.bot.send_photo(chat_id=Config.TELEGRAM_CHANNEL_ID, photo=open(chart_path, "rb"))

    async def error_handler(self, update, context):
        """Handle errors."""
        self.logger.error(f"Update {update} caused error {context.error}")
        if update:
            await update.message.reply_text("An error occurred. Please try again.")

    async def start(self):
        """Start the Telegram bot."""
        self.logger.info("Telegram bot started")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
