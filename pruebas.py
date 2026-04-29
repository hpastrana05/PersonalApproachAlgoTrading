from classes.data_manager import DataManager

dm = DataManager("AAPL", {"EMA": [10, 20], "RSI": [14], "SMA": [50], "WMA": [30], "BBands": [(20, 2)]}, "1m", "1D")

print(dm.data.tail())