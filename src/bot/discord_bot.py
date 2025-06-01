import discord
from discord.ext import commands
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.helpers import format_date
import pandas as pd
import os
from datetime import datetime, timedelta

class DiscordBot:
    def __init__(self, cmc_api, forex_api, ict_analysis, prediction, chart_generator):
        self.bot = commands.Bot(command_prefix="!")
        self.cmc_api = cmc_api
        self.forex_api = forex_api
        self.ict_analysis = ict_analysis
        self.prediction = prediction
        self.chart_generator = chart_generator
        self.logger = setup_logger()
        self.setup_handlers()

    def setup_handlers(self):
        @self.bot.command()
        async def analyze(ctx, symbol="BTC"):
            symbol = symbol.upper()
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
            
            data = self.cmc_api.get_historical_data(symbol, start_date, end_date)
            if not isinstance(data, pd.DataFrame):
                await ctx.send(f"Error fetching data for {symbol}.")
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
            await self.bot.get_channel(int(Config.DISCORD_CHANNEL_ID)).send(message)
            await self.bot.get_channel(int(Config.DISCORD_CHANNEL_ID)).send(file=discord.File(chart_path))

        @self.bot.command()
        async def forex(ctx, pair="EURUSD"):
            pair = pair.upper()
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
            
            data = self.forex_api.get_forex_data(pair, start_date, end_date)
            if not isinstance(data, pd.DataFrame):
                await ctx.send(f"Error fetching forex data for {pair}.")
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
            await self.bot.get_channel(int(Config.DISCORD_CHANNEL_ID)).send(message)
            await self.bot.get_channel(int(Config.DISCORD_CHANNEL_ID)).send(file=discord.File(chart_path))

        @self.bot.event
        async def on_ready():
            self.logger.info(f"Discord bot logged in as {self.bot.user}")

    def start(self):
        self.bot.run(Config.DISCORD_BOT_TOKEN)
