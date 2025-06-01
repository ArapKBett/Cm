import requests
import pandas as pd
from datetime import datetime
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.utils.helpers import normalize_data

class ForexData:
    def __init__(self):
        self.api_key = Config.ALPHA_VANTAGE_API_KEY
        self.base_url = "https://www.alphavantage.co/query"
        self.logger = setup_logger()

    def get_forex_data(self, pair, start_date, end_date):
        """Fetch historical forex data from Alpha Vantage."""
        try:
            # Split pair into from_currency and to_currency (e.g., EURUSD -> EUR/USD)
            from_currency = pair[:3]
            to_currency = pair[3:]
            
            # Alpha Vantage API parameters for daily forex data
            params = {
                "function": "FX_DAILY",
                "from_symbol": from_currency,
                "to_symbol": to_currency,
                "apikey": self.api_key,
                "outputsize": "full",  # Fetch all available data
                "datatype": "json"
            }
            
            self.logger.info(f"Fetching forex data for {pair} from {start_date} to {end_date}")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "Time Series FX (Daily)" not in data:
                self.logger.error(f"Error fetching forex data for {pair}: {data.get('Error Message', 'Unknown error')}")
                return None
            
            # Convert time series data to DataFrame
            time_series = data["Time Series FX (Daily)"]
            df_data = []
            for date, values in time_series.items():
                # Filter data within the specified date range
                if start_date <= date <= end_date:
                    df_data.append({
                        "date": date,
                        "open": float(values["1. open"]),
                        "high": float(values["2. high"]),
                        "low": float(values["3. low"]),
                        "close": float(values["4. close"]),
                        "volume": 0  # Alpha Vantage FX_DAILY does not provide volume
                    })
            
            if not df_data:
                self.logger.error(f"No forex data found for {pair} in the specified date range")
                return None
            
            df = pd.DataFrame(df_data)
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")  # Ensure chronological order
            self.logger.info(f"Retrieved {len(df)} forex data points for {pair}")
            return df
        
        except Exception as e:
            self.logger.error(f"Error fetching forex data for {pair}: {e}")
            return None
