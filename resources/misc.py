import time
from api_handler import get_market_month_close_unix_time, get_market_week_close_unix_time, get_market_day_close_unix_time
from stock_enums import TimeFrame

def candle_is_closed(timeframe: TimeFrame, candle_time):

    if timeframe == TimeFrame.DAY:
        close_time = get_market_day_close_unix_time(candle_time)
    elif timeframe == TimeFrame.WEEK:
        close_time = get_market_week_close_unix_time(candle_time)
    elif timeframe == TimeFrame.MONTH:
        close_time = get_market_month_close_unix_time(candle_time)

    current_unix_time = int(time.time())
    if current_unix_time > close_time:
        return True
    else:
        False

