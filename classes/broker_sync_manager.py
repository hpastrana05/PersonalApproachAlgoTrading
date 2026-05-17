from datetime import datetime

from trading_api import *

class BrokerSyncManager:

    def __init__(self, position):
        self.account: dict = None
        self.positions = {
            position.ticker: position
        }
        self.pending_orders = []

        self.last_sync_time = None
        self.is_synchronized = False

    def _sync_account_info(self):
        response = get_account_summary()

        if response:
            self.account  = {
                "cash": response["cash"],
                "currency": response["currency"],
                "investments": response["investments"],
                "total_value": response["total_value"] if "total_value" in response else 0,
            }

    def _sync_positions(self):
        
        for ticker, position in self.positions.items():
            response = get_all_open_positions(ticker)

            if response:
                position.update_from_response(response[0])
            else:
                position.update_as_closed()

    def _sync_pending_orders(self):
        response = get_pending_orders()

        self.pending_orders = response if response else []

    def sync(self):
        self.is_synchronized = False

        self._sync_account_info()
        self._sync_positions()
        self._sync_pending_orders()

        self.last_sync_time = datetime.now()
        self.is_synchronized = True

    def check_open_position(self, ticker: str) -> bool:
        if ticker in self.positions:
            return self.positions[ticker].position_open
        else:
            return False

    def check_pending_order(self, ticker: str, action: str) -> bool:
        for order in self.pending_orders:
            if order["ticker"] == ticker and order["side"] == action:
                return True
        return False

    def process_actions(self, ticker: str, action: str, price: float):
        if action == "BUY":
            self.sync()
            open_position = self.check_open_position(ticker)
            pending_order = self.check_pending_order(ticker, action)
            cash_available = self.account["cash"].availableToTrade

            if not open_position and not pending_order and cash_available > 1:
                quantity_to_buy = cash_available / price * 0.98
                post_place_market_order(quantity=quantity_to_buy, ticker=ticker)

        elif action == "SELL":
            self.sync()
            open_position = self.check_open_position(ticker)
            pending_order = self.check_pending_order(ticker, action)

            if open_position and not pending_order:
                quantity_to_sell = self.positions[ticker].quantity_available_for_trading
                post_place_market_order(quantity=-quantity_to_sell, ticker=ticker)
            
        elif action == "HOLD":
            self.sync()
            return
