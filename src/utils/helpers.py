from datetime import datetime
import pandas as pd

def format_date(date_str):
    """Format date string to ISO format."""
    return datetime.strptime(date_str, "%Y-%m-%d").isoformat()

def normalize_data(data, source="cmc"):
    """Normalize data into a standard DataFrame format."""
    if source == "cmc":
        return pd.DataFrame([
            {
                "date": d["quote"]["USD"]["timestamp"],
                "open": d["quote"]["USD"]["open"],
                "high": d["quote"]["USD"]["high"],
                "low": d["quote"]["USD"]["low"],
                "close": d["quote"]["USD"]["close"],
                "volume": d["quote"]["USD"]["volume"]
            } for d in data
        ])
    return pd.DataFrame(data)
