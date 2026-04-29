import logging

from trading_api import post_place_market_order

LOGGER = logging.getLogger("Position")

class Position:

    def __init__(self, ticker:str, action:str):
        self.ticker = ticker
        self.action = action

        self.position_open = False
        self.position_quantity = 0
    

    def open_position(self, quantity:int):
        if not self.position_open:
            LOGGER.info(f"Opening position: {self.action} {quantity} of {self.ticker}")

            quantity = quantity if self.action == "BUY" else -quantity

            response = post_place_market_order(quantity=quantity, ticker=self.ticker)

            if response== None:
                LOGGER.error(f"Failed to open position / place order: {self.action} {quantity} of {self.ticker}")
                return
            
            LOGGER.info(f"Position opened successfully: {self.action} {quantity} of {self.ticker}")
            self.position_open = True
            self.position_quantity = response["quantity"]


    def close_position(self):
        if self.position_open:
            LOGGER.info(f"Closing position: {self.action} {self.position_quantity} of {self.ticker}")

            quantity = -self.position_quantity if self.action == "BUY" else self.position_quantity

            response = post_place_market_order(quantity=quantity, ticker=self.ticker)

            if response == None:
                LOGGER.error(f"Failed to close position / place order: {self.action} {self.position_quantity} of {self.ticker}")
                return
        
            LOGGER.info(f"Position closed successfully: {self.action} {self.position_quantity} of {self.ticker}")
            self.position_open = False
            self.position_quantity = 0
