import json
import logging

from classes.strategy import Strategy
from classes.position import Position
from classes.data_manager import DataManager

LOGGER = logging.getLogger("StrategyManager")

class StrategyManager:

    def __init__(self, name:str, strategy:Strategy, position:Position, data_manager:DataManager):
        self.name = name
        self.strategy = strategy
        self.position = position
        self.data_manager = data_manager

        self.money = 0

    @classmethod
    def from_json(cls, file_path: str):
        try:
            with open(file_path, "r") as f:
                config = json.load(f)
                keys = config.keys()
                
                strategy = Strategy(
                    entry_signal=config["entry_rule"],
                    exit_signal=config["exit_rule"]
                )

                if "period" in keys:
                    period = config["period"]
                else:
                    period = None
                
                dm = DataManager(ticker = config["ticker_data"], 
                                indicators=config["indicators"], 
                                interval=config["interval"],
                                period=period)

                position = Position(ticker=config["ticker_API"], 
                                    action=config["action"])

            return cls(name=config["name"], strategy=strategy, position=position, data_manager=dm)
        
        except Exception as e:
            LOGGER.error(f"Error loading strategy from {file_path}: {e}")
            raise
            

    def update_market_data(self):
        LOGGER.info(f"Updating market data for {self.name}")
        self.data_manager.update_data()

    def check_strategy(self):
        if self.strategy.check_entry(self.data_manager.data):
            LOGGER.info(f"Entry signal triggered for {self.name}")
            return self.position.ticker, "BUY", self.data_manager.get_current_price()
        
        elif self.strategy.check_exit(self.data_manager.data):
            LOGGER.info(f"Exit signal triggered for {self.name}")
            return self.position.ticker, "SELL", self.data_manager.get_current_price()
        
        return self.position.ticker, "HOLD", self.data_manager.get_current_price()