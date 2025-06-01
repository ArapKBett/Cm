import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from src.utils.config import Config
from src.utils.logger import setup_logger
import os

class ChartGenerator:
    def __init__(self):
        self.logger = setup_logger()

    def generate_candlestick_chart(self, df, symbol, order_blocks, file_path):
        """Generate and save a candlestick chart with order blocks."""
        try:
            df = df.copy()
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            
            apds = [
                mpf.make_addplot(
                    [ob["price"]] * len(df),
                    type="hline",
                    color="red" if ob["type"] == "bearish" else "green",
                    linestyle="--"
                ) for ob in order_blocks
            ]
            
            os.makedirs(Config.CHART_DIR, exist_ok=True)
            mpf.plot(
                df,
                type="candle",
                style="yahoo",
                title=f"{symbol} Candlestick Chart",
                addplot=apds,
                savefig=file_path,
                figsize=(10, 6)
            )
            self.logger.info(f"Chart saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error generating chart for {symbol}: {e}")
