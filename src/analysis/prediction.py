from src.utils.logger import setup_logger

class Prediction:
    def __init__(self):
        self.logger = setup_logger()

    def predict_price(self, df, order_blocks, market_structure):
        """Generate price predictions using ICT concepts."""
        latest_price = df["close"].iloc[-1]
        prediction = {"direction": market_structure, "target": None}
        
        if market_structure == "Bullish":
            for ob in sorted(order_blocks, key=lambda x: x["price"]):
                if ob["type"] == "bullish" and ob["price"] > latest_price:
                    prediction["target"] = ob["price"]
                    break
        elif market_structure == "Bearish":
            for ob in sorted(order_blocks, key=lambda x: x["price"], reverse=True):
                if ob["type"] == "bearish" and ob["price"] < latest_price:
                    prediction["target"] = ob["price"]
                    break
        
        self.logger.info(f"Prediction for {market_structure}: Target {prediction['target'] or 'N/A'}")
        return prediction
