import time
import logging
from datetime import datetime, timedelta

from classes.trading_engine import TradingEngine

logging.basicConfig(
    filename="logs/algoTrading.log",
    format='%(asctime)s | %(name)s | %(levelname)s -> %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    level=logging.INFO
)

logging.getLogger("peewee").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)

logging.getLogger("StrategyManager").setLevel(logging.DEBUG)
logging.getLogger("Position").setLevel(logging.DEBUG)
logging.getLogger("DataManager").setLevel(logging.DEBUG)

LOGGER = logging.getLogger("Main")

def sleep_until_next_interval(minutes=1, second=1):
    now = datetime.now()
    next_minute_block = ((now.minute // minutes) + 1) * minutes

    if next_minute_block >= 60:
        next_run = (now.replace(minute=0, second=second, microsecond=0) + timedelta(hours=1))
    else:
        next_run = now.replace(minute=next_minute_block, second=second, microsecond=0)

    sleep_seconds = (next_run - now).total_seconds()
    time.sleep(max(sleep_seconds, 0))

def main():
    strategy_path = "strategies/strat_1.json"
    
    trading_engine = TradingEngine(strategy_path=strategy_path)

    
    while True:
        sleep_until_next_interval(minutes=1, second=1)

        LOGGER.debug(f"Running Strategy at {datetime.now()}")
        trading_engine.update_market_data()
        trading_engine.check_trading_strategy()


if __name__ == "__main__":
    main()
