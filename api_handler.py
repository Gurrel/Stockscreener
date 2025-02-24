import json
import requests
import pytz
from time import sleep
from multiprocessing import Manager
from datetime import datetime, timedelta, timezone
import pandas_market_calendars as mcal
from stock_enums import TimeFrame, CandleAttribute
from order_flow.candle import Candle
from locks import LockWarehouse


class ApiHandler:

    def __init__(self, api_key: str, data_manager, current_ticker: str):
    
        self.ticker = current_ticker
        self.api_key = api_key

        # Setting up the headers for authentication
        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        self.minute_data = data_manager.dict()
        self.daily_data = data_manager.dict()
        self.weekly_data = data_manager.dict()
        self.monthly_data = data_manager.dict()
        self.min5_data = data_manager.dict()
        self.latest_price = data_manager.Value('d', 0.0)
        self.latest_quote = data_manager.dict()


    def get_stock_data(self, time_frame: TimeFrame, time_units_back: int, locks: LockWarehouse):

        utc = pytz.timezone('UTC')
        today = datetime.now(tz=utc)
        today_str = today.strftime("%Y-%m-%d")

        if market_currently_past_open(today_str):
            end_date = today
        else:
            end_date = get_previous_trading_day(today)

        if time_frame == TimeFrame.DAY:
            start_date = end_date - timedelta(days=time_units_back)
        elif time_frame == TimeFrame.WEEK:
            start_date = end_date - timedelta(weeks=time_units_back)
        elif time_frame == TimeFrame.MONTH:
            start_date = end_date- timedelta(weeks=(time_units_back*5))
        elif time_frame == TimeFrame.MIN_5:
            start_date = get_month_market_open_date()
        elif time_frame == TimeFrame.MINUTES:
            start_date = end_date

        start_date = start_date.strftime("%Y-%m-%d")        
        end_date = end_date.strftime("%Y-%m-%d")



        max_retries = 10
        backoff_factor = 1.5

        for attempt in range(1, max_retries + 1):
            try:
                with locks.ticker:
                    ticker = self.ticker
                    url = f"https://api.marketdata.app/v1/stocks/candles/{time_frame.value}/{ticker}?from={start_date}&to={end_date}"

                print(f"Attempt {attempt}: Fetching data from {url}")
                response = requests.get(url, headers=self.headers)
                
                if response.status_code in (200, 203):
                    data = response.json()
                    data["fresh_trend"] = True
                    data["fresh_vwap"] = True
                    data["fresh_sma"] = True
                    data["fresh_zone"] = True
                    data["timeframe"] = time_frame.name
                    data["symbol"] = ticker
                    data = add_candles_to_dict(data)

                    #with open("bar_data.json", "w") as file:
                        #json.dump(data, file ,indent=4)

                    return data

                elif response.status_code >= 400 and response.status_code < 500:
                    print(f"Client Error {response.status_code}: {response.text}. Not retrying.")
                else:
                    print(f"Attempt {attempt} failed with status code {response.status_code}. Retrying...")
            except requests.RequestException as e:
                print(f"Attempt {attempt} failed due to network error: {e}. Retrying...")

            sleep((backoff_factor ** attempt) + (0.1 *attempt))                        

        print("All retry attempts failed. Returning None.")
        return None  # Return None after exhausting retries
        

        
    def get_candle_history_from_number_of_candles_back(self, candle_data_type: CandleAttribute, time_frame: TimeFrame, candles_back: int) -> list:

        data_point_history: list = []
        candle_data: json = None
        candle_data_type = candle_data_type.value

        if time_frame == TimeFrame.DAY:
            candle_data = self.daily_data
        elif time_frame == TimeFrame.WEEK:
            candle_data = self.weekly_data
        elif time_frame == TimeFrame.MONTH:
            candle_data = self.monthly_data
        elif time_frame == TimeFrame.MINUTES:
            candle_data = self.minute_data
        elif time_frame == TimeFrame.MIN_5:
            candle_data = self.min5_data

        candle_data: list = candle_data[candle_data_type]

        if type(candles_back) == int:
            if candles_back > len(candle_data):
                print("Error: Not enough data that far back")
                return None

        if candles_back == None:
            time_unit_skip = 0
        else:
            time_unit_skip = len(candle_data) - candles_back
            candle_data = candle_data[time_unit_skip:]

        for data_point in candle_data:
            data_point_history.append(data_point)

        return data_point_history
    
    def get_candle_data_from_unix_time(self, unix_time: int, time_frame: TimeFrame, candle_data_type: CandleAttribute) -> list:

        if time_frame == TimeFrame.DAY:
            local_candle_data = self.daily_data
        elif time_frame == TimeFrame.WEEK:
            local_candle_data = self.weekly_data
        elif time_frame == TimeFrame.MONTH:
            local_candle_data = self.monthly_data
        elif time_frame == TimeFrame.MINUTES:
            local_candle_data = self.minute_data
        elif time_frame == TimeFrame.MIN_5:
            local_candle_data = self.min5_data

        time_data_exists: bool = False

        for data_index, candle_time in enumerate(local_candle_data["t"]):
            if unix_time == candle_time:
                time_data_exists = True
                break

        if not time_data_exists:
            return None
        
        candle_data_type = candle_data_type.value
        candle_data_history: list = local_candle_data[candle_data_type]
        candle_data_history: list = candle_data_history[data_index:]
        
        return candle_data_history


    def fetch_stock_quote(self, ticker_lock):
        
        max_retries = 10
        backoff_factor = 1.5
        for attempt in range(1, max_retries + 1):
            try:
                with ticker_lock:
                    url = f"https://api.marketdata.app/v1/stocks/quotes/{self.ticker}/"
                response = requests.get(url, headers=self.headers)
                if response.status_code in (200, 203):
                    return response.json()
                
                elif response.status_code >= 400 and response.status_code < 500:
                    print(f"Client Error {response.status_code}: {response.text}. Not retrying.")
                else:
                    print(f"Attempt {attempt} failed with status code {response.status_code}. Retrying...")
            except requests.RequestException as e:
                print(f"Attempt {attempt} failed due to network error: {e}. Retrying...")

            sleep((backoff_factor ** attempt) + (0.1 *attempt))

        print("All retry attempts failed. Returning None.")
        return None      


def add_candles_to_dict(data: dict) -> dict:
    
    filtered_data = {k: v for k, v in data.items() if k in {"o", "h", "c", "l", "t"}}
    value_count = len(filtered_data["t"])
    data["candles"] = []

    for value_idx in range(value_count):
        temp_candle = Candle()
        temp_candle.timeframe = data["timeframe"]
        for key in filtered_data:
            if key == 'o':
                temp_candle.open = filtered_data[key][value_idx]
            elif key == 'h':
                temp_candle.high = filtered_data[key][value_idx]
            elif key == 'l':
                temp_candle.low = filtered_data[key][value_idx]
            elif key == 'c':
                temp_candle.close = filtered_data[key][value_idx]
            elif key == 't':
                # converts the unix time into a int
                temp_candle.time = int(filtered_data[key][value_idx])
        if value_idx != 0:
            temp_candle.previous_candle = previous_candle
        previous_candle = temp_candle

        data["candles"].append(temp_candle)

    return data



def get_week_market_open_unix_time(date: datetime = datetime.now(timezone.utc)) -> int:

    first_day_of_week = date - timedelta(days=date.weekday())
    first_day_of_week_str = first_day_of_week.strftime("%Y-%m-%d")

    if not open_market_day(first_day_of_week_str):
        first_market_day_of_week: datetime = get_next_market_day(first_day_of_week)
    else:
        first_market_day_of_week = first_day_of_week

    if date < first_market_day_of_week:
        previous_monday = date - timedelta(days=date.weekday()+7)
        return get_week_market_open_unix_time(previous_monday)


    open_hour, open_minute, timezone = get_market_open_time_from_date(first_market_day_of_week.strftime("%Y-%m-%d"))

    first_market_day_of_week = first_market_day_of_week.replace(hour=open_hour, minute=open_minute, second=0, microsecond=0, tzinfo=timezone)

    unix_time = int(first_market_day_of_week.timestamp())

    return unix_time


def get_month_market_open_unix_time() -> int:

    utc = pytz.timezone('UTC')
    today = datetime.now(tz=utc)
    today_str = today.strftime("%Y-%m-%d")

    if not open_market_day(today_str):
        active_date = get_previous_trading_day(today)
    else:
        active_date = today

    month_first_day = active_date.replace(day=1)
    month_first_day_str = month_first_day.strftime("%Y-%m-%d")

    if not open_market_day(month_first_day_str):
        first_market_day_of_month: datetime = get_next_market_day(month_first_day)
    else:
        first_market_day_of_month = month_first_day

    first_market_day_of_month_str = first_market_day_of_month.strftime("%Y-%m-%d")
    market_open_hour, market_open_minute, timezone = get_market_open_time_from_date(first_market_day_of_month_str)

    first_market_day_of_month = first_market_day_of_month.replace(hour=market_open_hour, minute=market_open_minute, second=0, microsecond=0, tzinfo=timezone)

    first_market_day_of_month = int(first_market_day_of_month.timestamp())

    return first_market_day_of_month

def get_month_market_open_date() -> datetime:

    utc = pytz.timezone('UTC')
    today = datetime.now(tz=utc)
    today_str = today.strftime("%Y-%m-%d")

    if not open_market_day(today_str):
        active_date = get_previous_trading_day(today)
    else:
        active_date = today

    month_first_day = active_date.replace(day=1)
    month_first_day_str = month_first_day.strftime("%Y-%m-%d")

    if not open_market_day(month_first_day_str):
        first_market_day_of_month: datetime = get_next_market_day(month_first_day)
    else:
        first_market_day_of_month = month_first_day

    first_market_day_of_month_str = first_market_day_of_month.strftime("%Y-%m-%d")
    market_open_hour, market_open_minute, timezone = get_market_open_time_from_date(first_market_day_of_month_str)

    first_market_day_of_month = first_market_day_of_month.replace(hour=market_open_hour, minute=market_open_minute, second=0, microsecond=0, tzinfo=timezone)

    return first_market_day_of_month


def get_current_market_open_unix_time() -> int:

    utc = pytz.timezone('UTC')
    today = datetime.now(tz=utc)
    today_str = today.strftime("%Y-%m-%d")

    if not open_market_day(today_str) or not market_currently_past_open(today_str):
        date = get_previous_trading_day(today)
    else:
        date = today
    date_str = date.strftime("%Y-%m-%d")

    market_open_hour, market_open_minute, timezone = get_market_open_time_from_date(date_str)
    date = date.replace(hour=market_open_hour, minute=market_open_minute, second=0, microsecond=0, tzinfo=timezone)
    unix_time = int(date.timestamp())

    return unix_time

 

def get_market_open_time_from_date(date: str):
    # Time is in UTC
    nyse = mcal.get_calendar("NYSE")
    schedule = nyse.schedule(start_date=date, end_date=date)

    if schedule.empty:
        print("Market not open ERROR: get_market_open_time_from_date")
        return None

    market_open: datetime.time = schedule["market_open"].iloc[0]
    timezone = market_open.tzinfo

    hour = market_open.hour
    minute = market_open.minute

    return hour, minute, timezone

def get_market_close_time_from_date(date: str):
    # Time is in UTC
    nyse = mcal.get_calendar("NYSE")
    schedule = nyse.schedule(start_date=date, end_date=date)

    if schedule.empty:
        print("Market not open ERROR: get_market_open_time_from_date")
        return None

    market_open: datetime.time = schedule["market_close"].iloc[0]
    timezone = market_open.tzinfo

    hour = market_open.hour
    minute = market_open.minute

    return hour, minute, timezone



def get_next_market_day(date: datetime) -> datetime:

    # NYSE calendar
    nyse = mcal.get_calendar("NYSE")
    
    while True:
        # Go forward one day
        date += timedelta(days=1)
        
        # Check if the date is a trading day
        date_str = date.strftime("%Y-%m-%d")  # Convert to string for mcal input
        result = nyse.schedule(start_date=date_str, end_date=date_str)
        
        if not result.empty:  # Found a valid trading day
            return date

def get_previous_trading_day(date: datetime) -> datetime:

    # NYSE calendar
    nyse = mcal.get_calendar("NYSE")
    
    while True:
        # Go back one day
        date -= timedelta(days=1)
        
        # Check if the date is a trading day
        date_str = date.strftime("%Y-%m-%d")  # Convert to string for mcal input
        result = nyse.schedule(start_date=date_str, end_date=date_str)
        
        if not result.empty:  # Found a valid trading day
            return date


def open_market_day(date: str):
    result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
    if result.empty == False:
        return True
    else:
        return False

def market_currently_past_open(date: str):

    schedule = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date) # GMT TIME

    if schedule.empty:
        return False

    market_open_date: datetime = schedule["market_open"].iloc[0]
    timezone = market_open_date.tzinfo
    
    market_open_time = market_open_date.time()
    market_close_time = schedule["market_close"].iloc[0].time()

    current_time = datetime.now(timezone).time()

    market_opening = (schedule.empty == False)

    if market_opening and current_time >= market_open_time:
        return True
    else:
        return False   
    
def market_currently_open(date: str):
    schedule = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date) # GMT TIME

    if schedule.empty:
        return False

    market_open_date: datetime = schedule["market_open"].iloc[0]
    timezone = market_open_date.tzinfo
    
    market_open_time = market_open_date.time()
    market_close_time = schedule["market_close"].iloc[0].time()

    current_time = datetime.now(timezone).time()

    market_opening = (schedule.empty == False)

    if market_opening and current_time >= market_open_time and current_time <= market_close_time:
        return True
    else:
        return False    


def get_market_month_close_unix_time(current_unix_time: int) -> int:
    date: datetime = datetime.fromtimestamp(current_unix_time, timezone.utc)
    
    last_day_of_month = date.replace(month=date.month+1) - timedelta(days=1)
    last_day_of_month_str = last_day_of_month.strftime("%Y-%m-%d")

    if not open_market_day(last_day_of_month_str):
        last_trading_day_of_month = get_previous_trading_day(last_day_of_month)
    else:
        last_trading_day_of_month = last_day_of_month

    hour, minute, tz = get_market_close_time_from_date(last_trading_day_of_month.strftime("%Y-%m-%d"))

    closing_date_of_month: datetime = last_trading_day_of_month.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=tz)
    closing_unix_time = int(closing_date_of_month.timestamp())
    
    return closing_unix_time

def get_market_week_close_unix_time(current_unix_time: int) -> int:
    date: datetime = datetime.fromtimestamp(current_unix_time, timezone.utc)
    days_until_friday = (4 - date.weekday()) % 7
    friday = date + timedelta(days=days_until_friday)
    friday_str = friday.strftime("%Y-%m-%d")

    if not open_market_day(friday_str):
        market_week_close: datetime = get_previous_trading_day(friday)
    else:
        market_week_close = friday
    
    hour, minute, tz = get_market_close_time_from_date(market_week_close.strftime("%Y-%m-%d"))
    market_week_close = market_week_close.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=tz)
    closing_unix_time = int(market_week_close.timestamp())

    return closing_unix_time

def get_market_day_close_unix_time(current_unix_time: int) -> int:
    date: datetime = datetime.fromtimestamp(current_unix_time, timezone.utc)
    hour, minute, tz = get_market_close_time_from_date(date.strftime("%Y-%m-%d"))
    closing_date = date.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=tz)
    closing_unix_time = int(closing_date.timestamp())
    return closing_unix_time


