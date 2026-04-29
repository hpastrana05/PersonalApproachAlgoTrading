from classes.strategy_manager import StrategyManager

class TradingEngine:

    def __init__(self, strategy_path: str):
        self.strategy_manager = StrategyManager.from_json(strategy_path)
    
    def update_market_data(self):
        self.strategy_manager.update_market_data()
    
    def check_trading_strategy(self):
        self.strategy_manager.check_strategy()

        