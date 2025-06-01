import requests
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.helpers import normalize_data

class CoinMarketCapAPI:
    def __init__(self):
        self.api_key = Config.COINMARKETCAP_API_KEY
        self.base_url = "https://pro-api.coinmarketcap.com"
        self.logger = setup_logger()

    def get_crypto_data(self, symbol, convert="USD"):
        """Fetch real-time crypto data."""
        url = f"{self.base_url}/v1/cryptocurrency/quotes/latest"
        headers = {"X-CMC_PRO_API_KEY": self.api_key}
        params = {"symbol": symbol, "convert": convert}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if "data" not in data or symbol not in data["data"]:
                self.logger.error(f"No data found for {symbol}")
                return None
            return data["data"][symbol]
        except Exception as e:
            self.logger.error(f"Error fetching crypto data for {symbol}: {e}")
            return None

    def get_historical_data(self, symbol, time_start, time_end, interval="daily"):
        """Fetch historical crypto data."""
        url = f"{self.base_url}/v1/cryptocurrency/ohlcv/historical"
        headers = {"X-CMC_PRO_API_KEY": self.api_key}
        params = {
            "symbol": symbol,
            "time_start": time_start,
            "time_end": time_end,
            "interval": interval
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if "data" not in data or symbol not in data["data"]:
                self.logger.error(f"No historical data found for {symbol}")
                return None
            return normalize_data(data["data"][symbol]["quotes"], source="cmc")
        except Exception as e:
            self.logger.error(f"Error fetching historical data for {symbol}: {e}")
            return None
