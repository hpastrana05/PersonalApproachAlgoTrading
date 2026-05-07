import logging

LOGGER = logging.getLogger("Position")

class Position:

    def __init__(self, ticker: str, action: str):
        self.ticker = ticker
        self.action = action

        self.position_open = False
        self.position_quantity = 0.0

        self.average_price_paid = None
        self.current_price = None
        self.created_at = None

        self.quantity_available_for_trading = 0.0
        self.quantity_in_pies = 0.0

        self.wallet_impact = None

        self.status = "FLAT"

    def update_from_response(self, response: dict):
        self.position_open = True
        self.position_quantity = response["quantity"]

        self.average_price_paid = response["averagePricePaid"]
        self.current_price = response["currentPrice"]
        self.created_at = response["createdAt"]

        self.quantity_available_for_trading = response["quantityAvailableForTrading"]
        self.quantity_in_pies = response["quantityInPies"]

        self.wallet_impact = response["walletImpact"]

        self.status = "OPEN"
    
    def update_as_closed(self):
        self.position_open = False
        self.status = "FLAT"
        self.position_quantity = 0

        self.average_price_paid = None
        self.current_price = None
        self.created_at = None

        self.quantity_available_for_trading = 0
        self.quantity_in_pies = 0

        self.wallet_impact = None