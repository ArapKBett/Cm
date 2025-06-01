import pandas as pd
from src.utils.logger import setup_logger

class ICTAnalysis:
    def __init__(self):
        self.logger = setup_logger()

    def find_order_blocks(self, df):
        """Identify order blocks (support/resistance zones)."""
        order_blocks = []
        df = df.copy()
        df["date"] = pd.to_datetime(df["date"])
        
        for i in range(2, len(df) - 2):
            # Bearish order block (potential resistance)
            if df["high"].iloc[i] > df["high"].iloc[i-1] and df["high"].iloc[i] > df["high"].iloc[i+1]:
                order_blocks.append({
                    "type": "bearish",
                    "price": df["high"].iloc[i],
                    "date": df["date"].iloc[i]
                })
            # Bullish order block (potential support)
            if df["low"].iloc[i] < df["low"].iloc[i-1] and df["low"].iloc[i] < df["low"].iloc[i+1]:
                order_blocks.append({
                    "type": "bullish",
                    "price": df["low"].iloc[i],
                    "date": df["date"].iloc[i]
                })
        self.logger.info(f"Found {len(order_blocks)} order blocks")
        return order_blocks

    def analyze_market_structure(self, df):
        """Analyze market structure (trend direction)."""
        df = df.copy()
        df["sma_20"] = df["close"].rolling(window=20).mean()
        df["sma_50"] = df["close"].rolling(window=50).mean()
        
        latest_close = df["close"].iloc[-1]
        sma_20 = df["sma_20"].iloc[-1]
        sma_50 = df["sma_50"].iloc[-1]
        
        if latest_close > sma_20 > sma_50:
            return "Bullish"
        elif latest_close < sma_20 < sma_50:
            return "Bearish"
        return "Neutral"
