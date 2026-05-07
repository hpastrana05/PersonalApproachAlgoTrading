from classes.broker_sync_manager import BrokerSyncManager
from classes.strategy_manager import StrategyManager

class TradingEngine:

    def __init__(self, strategy_path: str):
        self.strategy_manager = StrategyManager.from_json(strategy_path)
        position = self.strategy_manager.position
        self.broker_sync_manager = BrokerSyncManager(position)
    
    def update_market_data(self):
        self.strategy_manager.update_market_data()
    
    def check_trading_strategy(self):
        ticker, action, price = self.strategy_manager.check_strategy()
        self.broker_sync_manager.process_actions(ticker, action, price)

        