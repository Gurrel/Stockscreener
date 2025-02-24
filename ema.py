import time
from api_handler import ApiHandler
from locks import LockWarehouse
from stock_enums import TimeFrame, CandleAttribute, Position


def EMA_position(api_handler: ApiHandler, locks: LockWarehouse, time_frame: TimeFrame, ema_length: int):

    if time_frame == TimeFrame.DAY:
        data = api_handler.daily_data
        data_lock = locks.daily_data
    if time_frame == TimeFrame.WEEK:
        data = api_handler.weekly_data
        data_lock = locks.weekly_data
    if time_frame == TimeFrame.MONTH:
        data = api_handler.monthly_data
        data_lock = locks.monthly_data

    with locks.latest_quote:
        quote_price, quote_symbol = api_handler.latest_quote["last"][0], api_handler.latest_quote["symbol"][0]
    with data_lock:
        data_symbol = data["symbol"]

    if quote_symbol != data_symbol:
        print("quote_symbol and data_symbol does not match in SMA_position()")
        time.sleep(0.4)
        return EMA_position(api_handler, locks, time_frame, ema_length)

    with data_lock:
        closes = api_handler.get_candle_history_from_number_of_candles_back(CandleAttribute.CLOSE, time_frame, candles_back=None)

    if closes == None or len(closes) < ema_length:
        position = {"type": Position, "value": Position.NO_DATA.value, "text": Position.NO_DATA.value, "fresh": True}
        return position

    ema_price = calculate_EMA(closes, ema_length)
    ema_price = round(ema_price, 2)

    if quote_price > ema_price:
        position = Position.ABOVE.value
    else:
        position = Position.BELOW.value

    tooltip = f"price: {"{:.2f}".format(ema_price)}\ntimeframe: {time_frame.name}"
    return {"type": Position, "name": f"EMA {time_frame.value} {ema_length}", "value": position, "text": position, "price": ema_price, "tooltip": tooltip, "fresh": True}


def calculate_EMA(prices: list, length: int):
    alpha = 2 / (length + 1)

    initial_EMA = sum(prices[:length]) / length  

    ema = initial_EMA
    for price in prices[length:]:
        ema = alpha * price + (1 - alpha) * ema  

    return ema


def calculate_SMA(prices: list):
    sma = sum(prices) / len(prices)
    return sma
