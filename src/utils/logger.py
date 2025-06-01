import logging
import os
from src.utils.config import Config

def setup_logger():
    os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
    logging.basicConfig(
        filename=Config.LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("CryptoICTBot")
