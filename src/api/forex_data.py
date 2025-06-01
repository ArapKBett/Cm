import pandas as pd
from datetime import datetime, timedelta
from src.utils.logger import setup_logger

class ForexData:
    def __init__(self):
        self.logger = setup_logger()

    def get_forex_data(self, pair, start_date, end_date):
        """Mock forex data retrieval."""
        self.logger.info(f"Fetching mock forex data for {pair}")
        dates = pd.date_range(start=start_date, end=end_date, freq="D")
        data = {
            "date": dates,
            "open": [1.1 + i * 0.01 for i in range(len(dates))],
            "high": [1.12 + i * 0.01 for i in range(len(dates))],
            "low": [1.08 + i * 0.01 for i in range(len(dates))],
            "close": [1.1 + i * 0.01 for i in range(len(dates))],
            "volume": [1000 + i * 10 for i in range(len(dates))]
        }
        return pd.DataFrame(data)
