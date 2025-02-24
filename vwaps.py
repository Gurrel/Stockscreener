import time
from stock_enums import Position, TimeFrame, CandleAttribute
import datetime as dt
import numpy as np
from api_handler import ApiHandler, get_week_market_open_unix_time, get_month_market_open_unix_time, get_current_market_open_unix_time
from locks import LockWarehouse


def get_VWAP_position(api_handler: ApiHandler, locks: LockWarehouse, timeframe: TimeFrame) -> dict:

    if timeframe == TimeFrame.DAY:
        unix_time = get_current_market_open_unix_time()
        data_lock = locks.minute_data
        with data_lock:
            data = api_handler.minute_data        
        data_timeframe = TimeFrame.MINUTES
    elif timeframe == TimeFrame.WEEK:
        unix_time = get_week_market_open_unix_time()
        data_lock = locks.min5_data
        with data_lock:
            data = api_handler.min5_data
        data_timeframe = TimeFrame.MIN_5
    elif timeframe == TimeFrame.MONTH:
        unix_time = get_month_market_open_unix_time()
        data_lock = locks.min5_data
        with data_lock:
            data = api_handler.min5_data
        data_timeframe = TimeFrame.MIN_5

    with data_lock:
        closes = api_handler.get_candle_data_from_unix_time(unix_time, data_timeframe, CandleAttribute.CLOSE)
        highs = api_handler.get_candle_data_from_unix_time(unix_time, data_timeframe, CandleAttribute.HIGH)
        lows = api_handler.get_candle_data_from_unix_time(unix_time, data_timeframe, CandleAttribute.LOW)
        volumes = api_handler.get_candle_data_from_unix_time(unix_time, data_timeframe, CandleAttribute.VOLUME)        
        data_symbol = data["symbol"]

    with locks.latest_quote:
        quote_price, quote_symbol = api_handler.latest_quote["last"][0], api_handler.latest_quote["symbol"][0]

    if data_symbol != quote_symbol:
        print(f"quote_symbol {quote_symbol} and data_symbol {data_symbol} does not match in {get_VWAP_position.__name__}, timeframe: {timeframe}")
        time.sleep(0.4)
        return get_VWAP_position(api_handler, locks, timeframe) 

    vwap_price, upper_band, lower_band = calculate_VWAP(closes, volumes, highs, lows)

    range = upper_band - lower_band
    midpoint = lower_band + (range / 2)
    relative_price = quote_price - midpoint
    percentage = round((relative_price / (range / 2)) * 100)
    percentage_str = f"{percentage}%"

    if quote_price > vwap_price:
        position = Position.ABOVE.value
    else:
        position = Position.BELOW.value

    vwap_price_str = f"{vwap_price:.2f}"
    upper_band_str = f"{upper_band:.2f}"
    lower_band_str = f"{lower_band:.2f}"
    vwap_price = round(vwap_price, 2)

    tooltip = (
        f"price: {vwap_price_str}\n"
        f"position: {position}\n"
        f"upper band: {upper_band_str}\n"
        f"lower band: {lower_band_str}\n"
        f"timeframe: {timeframe.name}"
    )

    return {"type": "vwap", "name": f"VWAP {timeframe.value}", "value": percentage, "text": percentage_str, "price": vwap_price, "tooltip": tooltip, "fresh": True}


def calculate_VWAP(closes: list, volumes: list, highs: list, lows: list, k: int = 1):

    closes = np.array(closes, dtype=np.float64)
    volumes = np.array(volumes, dtype=np.float64)
    highs = np.array(highs, dtype=np.float64)
    lows = np.array(lows, dtype=np.float64)
    typical_price = (highs + lows + closes) / 3

    # Check for mismatched array lengths
    if not (len(closes) == len(volumes) == len(highs) == len(lows)):
        raise ValueError("Input lists must have the same length.")

    # Calculate VWAP
    vwap = np.sum(typical_price * volumes) / np.sum(volumes)
    
    # Calculate VWAP standard deviation
    variance = np.sum(volumes * (typical_price - vwap) ** 2) / np.sum(volumes)
    std_vwap = np.sqrt(variance)
    
    # Calculate VWAP bands
    upper_band = vwap + k * std_vwap
    lower_band = vwap - k * std_vwap
    
    return vwap, upper_band, lower_band

