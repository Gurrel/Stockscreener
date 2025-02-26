import threading
import time
from multiprocessing import Process, Queue, Manager
import tkinter as tk
from api_handler import ApiHandler
from gui.stockscreener import stockScreener
from locks import LockWarehouse
from queues import QueueWarehouse
from stock_enums import *
from ticker_reading.ocr_handling import ocr_thread, get_current_ticker
from ticker_reading.screen_selection import ScreenSelector
from vwaps import get_VWAP_position
from ema import EMA_position
from trends.macro_trend import get_macro_trend
from order_flow.zone_analysis import find_zone_data
from previous_bars import get_inside_previous_candle_data
from resources.stock_data_store import StockDataStore



def run_screen_selection(root: tk.Tk, region_queue: Queue):
    selector = ScreenSelector(root)
    selection = selector.run()
    region_queue.put(selection)

    
def poll_ticker_ocr_handler(queues: QueueWarehouse, app: stockScreener, api_handler: ApiHandler, ticker_lock):

    if not queues.ticker.empty():
        with ticker_lock:
            api_handler.ticker = queues.ticker.get()
            
        app.widgets_to_loading_state()
            

    app.root.after(100, poll_ticker_ocr_handler, queues, app, api_handler, ticker_lock)



def start_api_threads(api_handler: ApiHandler, locks: LockWarehouse, queues: QueueWarehouse):

    daily_data_thread = threading.Thread(target=daily_candles_api_thread, args=(api_handler, locks,), daemon=True)
    daily_data_thread.start()

    weekly_data_thread = threading.Thread(target=weekly_candles_api_thread, args=(api_handler, locks,), daemon=True)
    weekly_data_thread.start()

    monthly_data_thread = threading.Thread(target=monthly_candles_api_thread, args=(api_handler, locks,), daemon=True)
    monthly_data_thread.start()

    min5_data_thread = threading.Thread(target=min5_candles_api_thread, args=(api_handler, locks,), daemon=True)
    min5_data_thread.start()

    minute_data_thread = threading.Thread(target=minute_candles_api_thread, args=(api_handler, locks,), daemon=True)
    minute_data_thread.start()

    quote_data_thread = threading.Thread(target=stock_quote_thread, args=(api_handler, queues, locks,), daemon=True)
    quote_data_thread.start()

def daily_candles_api_thread(api_handler: ApiHandler, locks: LockWarehouse):
    while True:
        update_time = 600

        with locks.ticker:
            current_ticker = api_handler.ticker

        candle_data = api_handler.get_stock_data(TimeFrame.DAY, 1000, locks)

        with locks.daily_data:
            api_handler.daily_data.clear()
            api_handler.daily_data.update(candle_data)
            data = api_handler.daily_data
            print(f"Daily Data in thread: {data['c'][len(data)-20:]}")


        time_passed: int = 0
        while time_passed < update_time:
            with locks.ticker:
                latest_ticker = api_handler.ticker

            if latest_ticker != current_ticker:
                break

            time.sleep(0.1)
            time_passed += 0.1


def weekly_candles_api_thread(api_handler: ApiHandler, locks: LockWarehouse):
    while True:
        update_time = 600

        with locks.ticker: 
            current_ticker = api_handler.ticker

        candle_data = api_handler.get_stock_data(TimeFrame.WEEK, 1000, locks)

        with locks.weekly_data:
            api_handler.weekly_data.clear()
            api_handler.weekly_data.update(candle_data)
            
        time_passed: int = 0
        while time_passed < update_time:
            with locks.ticker:
                latest_ticker = api_handler.ticker

            if latest_ticker != current_ticker:
                break

            time.sleep(0.1)
            time_passed += 0.1


def monthly_candles_api_thread(api_handler: ApiHandler, locks: LockWarehouse):
    while True:
        update_time = 600

        with locks.ticker:
            current_ticker = api_handler.ticker

        candle_data = api_handler.get_stock_data(TimeFrame.MONTH, 450, locks)

        with locks.monthly_data:
            api_handler.monthly_data.clear()
            api_handler.monthly_data.update(candle_data)

        time_passed: int = 0
        while time_passed < update_time:
            with locks.ticker:
                latest_ticker = api_handler.ticker

            if latest_ticker != current_ticker:
                break

            time.sleep(0.1)
            time_passed += 0.1

def min5_candles_api_thread(api_handler: ApiHandler, locks: LockWarehouse):
    while True:
        update_time = 100

        with locks.ticker:
            current_ticker = api_handler.ticker

        candle_data = api_handler.get_stock_data(TimeFrame.MIN_5, None, locks)

        with locks.min5_data:
            api_handler.min5_data.clear()
            api_handler.min5_data.update(candle_data)

        with locks.ticker: 
            latest_ticker = api_handler.ticker

        time_passed: int = 0
        while time_passed < update_time:
            with locks.ticker:
                latest_ticker = api_handler.ticker

            if latest_ticker != current_ticker:
                break

            time.sleep(0.1)
            time_passed += 0.1


def minute_candles_api_thread(api_handler: ApiHandler, locks: LockWarehouse):
    while True:
        update_time = 100
        with locks.ticker:
            current_ticker = api_handler.ticker

        candle_data = api_handler.get_stock_data(TimeFrame.MINUTES, None, locks)

        with locks.minute_data:
            api_handler.minute_data.clear()
            api_handler.minute_data.update(candle_data)
            with locks.latest_price:
                api_handler.latest_price.value = candle_data["c"][-1] # most recent close

        time_passed: int = 0
        while time_passed < update_time:
            with locks.ticker:
                latest_ticker = api_handler.ticker

            if latest_ticker != current_ticker:
                break

            time.sleep(0.1)
            time_passed += 0.1

def stock_quote_thread(api_handler: ApiHandler, queues: QueueWarehouse, locks: LockWarehouse):
    update_time = 60
    with locks.ticker:
        new_ticker = api_handler.ticker
        current_ticker = api_handler.ticker
    while True:

        with locks.latest_quote:
            api_handler.latest_quote.clear()
            api_handler.latest_quote.update(api_handler.fetch_stock_quote(locks.ticker))
            last_price = api_handler.latest_quote["last"][0]
            last_price = "{:.2f}".format(last_price)
            quote_data = {"type": "quote", "value": last_price, "text": last_price, "tooltip": None, "fresh": True}
            queues.quote_price.put(quote_data)

        time_passed: int = 0
        while time_passed < update_time:
            with locks.ticker:
                new_ticker = api_handler.ticker
            if new_ticker != current_ticker:
                break

            time.sleep(0.1)
            time_passed += 0.1


def start_data_calculation_processes(root: tk.Tk, api_handler: ApiHandler, locks: LockWarehouse, queues: QueueWarehouse):

    if not fetched_all_api_data(root, api_handler, locks, queues):
        return

    vwap_process = Process(target=vwap_thread, args=(api_handler, locks, queues.vwap_d, queues.vwap_w, queues.vwap_m,), daemon=True)
    vwap_process.start()

    sma_process = Process(target=sma_thread, args=(api_handler, locks, queues,), daemon=True)
    sma_process.start()

    trend_process = Process(target=trend_thread, args=(api_handler, locks, queues,), daemon=True)
    trend_process.start()

    zone_process = Process(target=zone_thread, args=(api_handler, locks, queues,), daemon=True)
    zone_process.start()


def fetched_all_api_data(root: tk.Tk, api_handler: ApiHandler, locks: LockWarehouse, queues: QueueWarehouse):

    with locks.daily_data:
        with locks.weekly_data:
            with locks.monthly_data:
                with locks.min5_data:
                    with locks.minute_data:
                        with locks.latest_quote:
                            data_lengths = [len(api_handler.minute_data),len(api_handler.min5_data), len(api_handler.daily_data), len(api_handler.weekly_data), len(api_handler.monthly_data), len(api_handler.latest_quote)]
                            print(f"data length {data_lengths}")
                            if any(length == 0 for length in data_lengths):
                                root.after(500, start_data_calculation_processes, root, api_handler, locks, queues)
                                return False
                            else:
                                return True
    

def vwap_thread(api_handler: ApiHandler, locks: LockWarehouse, q_vwap_d: Queue, q_vwap_w: Queue, q_vwap_m: Queue):
    
    while True:

        with locks.minute_data:
            fresh_data = api_handler.minute_data["fresh_vwap"]
        if fresh_data:
            d_vwap_position = get_VWAP_position(api_handler, locks, TimeFrame.DAY)
            q_vwap_d.put(d_vwap_position)

        with locks.min5_data:
            fresh_data = api_handler.min5_data["fresh_vwap"]
        if fresh_data:
            m_vwap_position = get_VWAP_position(api_handler, locks, TimeFrame.MONTH)
            q_vwap_m.put(m_vwap_position)

        with locks.min5_data:
            fresh_data = api_handler.min5_data["fresh_vwap"]
        if fresh_data:
            w_vwap_position = get_VWAP_position(api_handler, locks, TimeFrame.WEEK)
            q_vwap_w.put(w_vwap_position)

        with locks.minute_data:
            api_handler.minute_data.update({"fresh_vwap": False})
        with locks.min5_data:
            api_handler.min5_data.update({"fresh_vwap": False})

        time.sleep(0.1)


def sma_thread(api_handler: ApiHandler, locks: LockWarehouse, queues: QueueWarehouse):

    while True:
        with locks.daily_data:
            fresh_data = api_handler.daily_data["fresh_sma"]
        if fresh_data:
            sma20_d_position: str = EMA_position(api_handler, locks, TimeFrame.DAY, ema_length=20)
            queues.sma20_d.put(sma20_d_position)
            sma50_d_position: str = EMA_position(api_handler, locks, TimeFrame.DAY, ema_length=50)
            queues.sma50_d.put(sma50_d_position)        
            sma200_d_position: str = EMA_position(api_handler, locks, TimeFrame.DAY, ema_length=200)
            queues.sma200_d.put(sma200_d_position)    
            api_handler.daily_data["fresh_sma"] = False

        with locks.weekly_data:
            fresh_data = api_handler.weekly_data["fresh_sma"]
        if fresh_data:
            sma20_w_position: str = EMA_position(api_handler, locks, TimeFrame.WEEK, ema_length=20)
            queues.sma20_w.put(sma20_w_position)
            sma50_w_position: str = EMA_position(api_handler, locks, TimeFrame.WEEK, ema_length=50)
            queues.sma50_w.put(sma50_w_position)
            sma200_w_position: str = EMA_position(api_handler, locks, TimeFrame.WEEK, ema_length=200)
            queues.sma200_w.put(sma200_w_position)
            api_handler.weekly_data["fresh_sma"] = False

        with locks.monthly_data:
            fresh_data = api_handler.monthly_data["fresh_sma"]
        if fresh_data:
            sma20_m_position: str = EMA_position(api_handler, locks, TimeFrame.MONTH, ema_length=20)
            queues.sma20_m.put(sma20_m_position)
            sma50_m_position: str = EMA_position(api_handler, locks, TimeFrame.MONTH, ema_length=50)
            queues.sma50_m.put(sma50_m_position)
            sma200_m_position: str = EMA_position(api_handler, locks, TimeFrame.MONTH, ema_length=200)
            queues.sma200_m.put(sma200_m_position)
            api_handler.monthly_data["fresh_sma"] = False

        time.sleep(0.1)


def trend_thread(api_handler: ApiHandler, locks: LockWarehouse, queues: QueueWarehouse):

    while True:   
        with locks.daily_data:
            fresh_data = api_handler.daily_data["fresh_trend"]
            if fresh_data:
                daily_closes = api_handler.get_candle_history_from_number_of_candles_back(CandleAttribute.CLOSE, TimeFrame.DAY, candles_back=None)
                last_candle_open_time = api_handler.get_candle_history_from_number_of_candles_back(CandleAttribute.TIME, TimeFrame.DAY, candles_back=1)[0]
                daily_trend: dict = get_macro_trend(daily_closes, last_candle_open_time, TimeFrame.DAY)
                queues.trend_d.put(daily_trend)
                api_handler.daily_data["fresh_trend"] = False

        with locks.weekly_data:
            fresh_data = api_handler.weekly_data["fresh_trend"]
            if fresh_data:
                weekly_closes = api_handler.get_candle_history_from_number_of_candles_back(CandleAttribute.CLOSE, TimeFrame.WEEK, candles_back=None)
                last_candle_open_time = api_handler.get_candle_history_from_number_of_candles_back(CandleAttribute.TIME, TimeFrame.WEEK, candles_back=1)[0]
                weekly_trend = get_macro_trend(weekly_closes, last_candle_open_time, TimeFrame.WEEK)
                queues.trend_w.put(weekly_trend)
                api_handler.weekly_data["fresh_trend"] = False

        with locks.monthly_data:
            fresh_data = api_handler.monthly_data["fresh_trend"]
            if fresh_data:
                monthly_closes = api_handler.get_candle_history_from_number_of_candles_back(CandleAttribute.CLOSE, TimeFrame.MONTH, candles_back=None)
                last_candle_open_time = api_handler.get_candle_history_from_number_of_candles_back(CandleAttribute.TIME, TimeFrame.MONTH, candles_back=1)[0]
                monthly_trend = get_macro_trend(monthly_closes, last_candle_open_time, TimeFrame.MONTH)
                queues.trend_m.put(monthly_trend)
                api_handler.monthly_data["fresh_trend"] = False

        time.sleep(0.1)

def zone_thread(api_handler: ApiHandler, locks: LockWarehouse, queues: QueueWarehouse):

    while True:

        with locks.daily_data:
            fresh_data, data_symbol = api_handler.daily_data["fresh_zone"], api_handler.daily_data["symbol"]
            with locks.latest_quote:
                last_price, quote_symbol = api_handler.latest_quote["last"][0], api_handler.latest_quote["symbol"][0]  
            if fresh_data and data_symbol == quote_symbol:
                closest_d_zone_data, inside_zone_d_data, daily_zones = find_zone_data(api_handler.daily_data, last_price)
                queues.closer_to_d.put(closest_d_zone_data)
                queues.inside_zone_d.put(inside_zone_d_data)
                queues.zones_d.put(daily_zones)
                inside_prev_bar_data_d = get_inside_previous_candle_data(api_handler.daily_data, last_price)
                queues.prev_bar_d.put(inside_prev_bar_data_d)
                api_handler.daily_data["fresh_zone"] = False

        with locks.weekly_data:
            fresh_data, data_symbol = api_handler.weekly_data["fresh_zone"], api_handler.weekly_data["symbol"]
            with locks.latest_quote:
                last_price, quote_symbol = api_handler.latest_quote["last"][0], api_handler.latest_quote["symbol"][0]
            if fresh_data and data_symbol == quote_symbol:
                closest_w_zone_data, inside_zone_w_data, weekly_zones = find_zone_data(api_handler.weekly_data, last_price)
                queues.closer_to_w.put(closest_w_zone_data)
                queues.inside_zone_w.put(inside_zone_w_data)
                queues.zones_w.put(weekly_zones)
                inside_prev_bar_data_w = get_inside_previous_candle_data(api_handler.weekly_data, last_price)
                queues.prev_bar_w.put(inside_prev_bar_data_w)
                api_handler.weekly_data["fresh_zone"] = False

        with locks.monthly_data:
            fresh_data, data_symbol = api_handler.monthly_data["fresh_zone"], api_handler.monthly_data["symbol"]
            with locks.latest_quote:
                last_price, quote_symbol = api_handler.latest_quote["last"][0], api_handler.latest_quote["symbol"][0]
            if fresh_data and data_symbol == quote_symbol:
                closest_m_zone_data, inside_zone_m_data, monthly_zones = find_zone_data(api_handler.monthly_data, last_price)
                queues.closer_to_m.put(closest_m_zone_data)
                queues.inside_zone_m.put(inside_zone_m_data)
                queues.zones_m.put(monthly_zones)
                inside_prev_bar_data_m = get_inside_previous_candle_data(api_handler.monthly_data, last_price)
                queues.prev_bar_m.put(inside_prev_bar_data_m)
                api_handler.monthly_data["fresh_zone"] = False

        time.sleep(0.1)

def start_app(root: tk.Tk, start_var: tk.BooleanVar, queues: QueueWarehouse):

    run_screen_selection(root, queues.ticker_region)
    start_var.set(True)

def update_data_store(root, data_store: StockDataStore, queues: QueueWarehouse):

    queues_in_order = queues.queues_in_order

    # Get dictionary of all attributes in the data store
    attributes = list(vars(data_store).keys())

    for i, queue in enumerate(queues_in_order):
        if not queue.empty() and i < len(attributes):  # Ensure we don't go out of bounds
            received_data = queue.get()
            setattr(data_store, attributes[i], received_data)  # Dynamically update the attribute

    root.after(100, update_data_store, root, data_store, queues)
            

def run_stock_screener():
    API_KEY = ""  
    manager = Manager()
    root = tk.Tk()
    app = stockScreener(root, API_KEY)
    queues = QueueWarehouse()
    started_app= tk.BooleanVar(value=False)
    root.update()
    app.start_btn.config(command=lambda: start_app(root, started_app, queues))
    app.start_btn.wait_variable(started_app)

    app.ocr_window_btn.config(command=lambda: run_screen_selection(root, queues.ticker_region))

    
    current_ticker = get_current_ticker(queues.ticker_region)

    api_handler = ApiHandler(API_KEY, manager, current_ticker)

    locks = LockWarehouse(manager)
    
    ticker_process = Process(target=ocr_thread, args=(queues.ticker, current_ticker, queues.ticker_region,), daemon=True)
    ticker_process.start()

    poll_ticker_ocr_handler(queues, app, api_handler, locks.ticker)
    start_api_threads(api_handler, locks, queues)

    start_data_calculation_processes(root, api_handler, locks, queues)

    app.update(queues, locks, api_handler)

    root.mainloop()



if __name__ == "__main__":
    try:
        run_stock_screener()
    except KeyboardInterrupt:
        print("Stopped program..")


    