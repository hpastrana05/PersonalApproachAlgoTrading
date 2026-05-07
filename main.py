import time
import logging

from classes.trading_engine import TradingEngine

logging.basicConfig(
    filename="logs/algoTrading.log", 
    format='%(asctime)s | %(name)s | %(levelname)s -> %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.DEBUG
)


def main():
    strategy_path = "strategies/strat_1.json"
    
    trading_engine = TradingEngine(strategy_path=strategy_path)

    
    while True:
        trading_engine.update_market_data()

        trading_engine.check_trading_strategy()



        time.sleep(1)


if __name__ == "__main__":
    main()
