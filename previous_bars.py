from __future__ import annotations
from typing import TYPE_CHECKING
from api_handler import ApiHandler
from stock_enums import PreviousBar

if TYPE_CHECKING:
    from order_flow.zone_analysis import Candle
    from locks import LockWarehouse


def get_inside_previous_candle_data(data: dict, current_price: float):
    
    prev_candle: Candle = data["candles"][-2]
    high = prev_candle.high
    low = prev_candle.low

    range = high - low
    midpoint = low + (range / 2)
    relative_price = current_price - midpoint

    percentage = round((relative_price / (range / 2)) * 100)
    percentage_str = str(percentage) + "%"

    if current_price <= high and current_price >= low:
        tooltip_val = PreviousBar.INSIDE.value
    else:
        tooltip_val = PreviousBar.OUTSIDE.value

    high_str = "{:.2f}".format(high)
    low_str = "{:.2f}".format(low)
    tooltip = f"Status: {tooltip_val}\n high: {high_str}\nlow: {low_str}\n timeframe: {prev_candle.timeframe}"

    inside_data = {"type": PreviousBar.RANGE, "value": percentage, "text": percentage_str, "tooltip": tooltip, "fresh": True}
    return inside_data