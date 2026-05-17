import pandas_ta as ta


def ema_cross_above(data, fast, slow):
    """Checks when the fast crosses slow from below to above"""
    cross = ta.cross(data[f"EMA_{fast}"], data[f"EMA_{slow}"], above=True, equal=False)
    return cross.iloc[-2] == 1


def ema_cross_below(data, fast, slow):
    """Checks when the fast crosses slow from above to below"""
    cross = ta.cross(data[f"EMA_{fast}"], data[f"EMA_{slow}"], above=False, equal=False)
    return cross.iloc[-2] == 1

def tp_percentage(data, position, percentage):
    """Checks if the current price is above the entry price by a certain percentage"""

    entry_price = position.position_quantity
    current_price = data["close"].iloc[-1]
    target_price = entry_price * (1 + percentage / 100)
    return current_price >= target_price

def sl_percentage(data, position, percentage):
    """Checks if the current price is below the entry price by a certain percentage"""
    entry_price = position.position_quantity
    current_price = data["close"].iloc[-1]
    stop_loss_price = entry_price * (1 - percentage / 100)
    return current_price <= stop_loss_price