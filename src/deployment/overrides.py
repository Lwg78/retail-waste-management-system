from datetime import datetime, timedelta

class OverrideManager:
    """
    Manages human overrides for model predictions with AUTO-EXPIRY.
    
    Why: Solves the "Stale Config" problem where managers forget to turn off overrides.
    [cite: 260, 268]
    """
    def __init__(self):
        # Stores overrides: key=(product_id, store_id), value={multiplier, expiry}
        self.overrides = {} 

    def set_override(self, product_id, store_id, multiplier, days_valid=7):
        """
        Manager sets an override (e.g., 1.2x demand) for a specific duration.
        """
        expiry_date = datetime.now() + timedelta(days=days_valid)
        self.overrides[(product_id, store_id)] = {
            'multiplier': multiplier,
            'expiry': expiry_date,
            'reason': 'User Input' # [cite: 255]
        }
        print(f"Override set for Product {product_id}: {multiplier}x until {expiry_date}")

    def get_effective_prediction(self, product_id, store_id, model_prediction):
        """
        Applies override if it exists and hasn't expired.
        """
        key = (product_id, store_id)
        
        if key in self.overrides:
            config = self.overrides[key]
            if datetime.now() < config['expiry']:
                # Apply active override
                return model_prediction * config['multiplier']
            else:
                # Clean up expired override [cite: 260]
                del self.overrides[key]
                return model_prediction
        
        return model_prediction