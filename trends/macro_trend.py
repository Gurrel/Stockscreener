import time
import trends.linked_queue as lq
from trends.enums import CurrentPosition
from stock_enums import Trend, TimeFrame
import numpy as np
from order_flow.zone_analysis import get_data
import matplotlib.pyplot as plt
from resources.misc import candle_is_closed


class QueueIsEmpty(Exception):
    def __init__(self, macro_trend: Trend = None):
        self.macro_trend = macro_trend


class BrokeUpperLevel(Exception):
    def __init__(self, current_close: float, peak_close: float, macro_trend: Trend):
        self.current_close = current_close  
        self.peak_close = peak_close
        self.macro_trend = macro_trend

class BrokeLowerLevel(Exception):
    def __init__(self, current_close: float, trough_close: float, macro_trend: Trend):
        self.current_close = current_close
        self.trough_close = trough_close
        self.macro_trend = macro_trend

def get_candle_trend(previous_close: float, next_close: float) -> str:

    if next_close > previous_close:
        return Trend.UP
    elif next_close < previous_close:
        return Trend.DOWN
    
    return Trend.SIDEWAYS


def data_to_queue(price_data: list):

    q = lq.LinkedQ()

    for price in price_data:
        q.enqueue(price)

    return q


def get_initial_candle_trend(q: lq.LinkedQ):
    previous_close = q.dequeue()
    current_close = q.dequeue()
    candle_trend = get_candle_trend(previous_close, current_close)
    return candle_trend, current_close



def find_peak(q: lq.LinkedQ, current_close: float):

    if q.isEmpty():
        raise QueueIsEmpty("Not enough data for trend analysis")

    next_close = q.peek()

    if next_close >= current_close:
        current_close = q.dequeue()
        return find_peak(q, current_close)
    elif next_close < current_close:
        peak_close = current_close
        return peak_close
    

def find_trough(q: lq.LinkedQ, current_close: float):

    if q.isEmpty():
        raise QueueIsEmpty("Not enough data for trend analysis")

    next_close = q.peek()

    if next_close <= current_close:
        current_close = q.dequeue()
        return find_trough(q, current_close)
    elif next_close > current_close:
        trough_close = current_close
        return trough_close
    

def calculate_trend(# -----------------------------------) -> Trend:

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------

    

def find_peak_then_trough(q: lq.LinkedQ, current_close: float):

    peak_close = find_peak(q, current_close)
    trough_close = find_trough(q, current_close=peak_close)

    return peak_close, trough_close



def find_trough_then_peak(q: lq.LinkedQ, current_close: float):

    trough_close = find_trough(q, current_close)
    peak_close = find_peak(q, current_close=trough_close)

    return peak_close, trough_close
        

def get_initial_controlling_highs_and_lows(q: lq.LinkedQ):

    initial_candle_trend, current_close = get_initial_candle_trend(q)

    if initial_candle_trend == Trend.UP:

        peak, trough = find_peak_then_trough(q, current_close)
        current_close = trough
        current_position = CurrentPosition.TROUGH

    elif initial_candle_trend == Trend.DOWN:

        peak, trough = find_trough_then_peak(q, current_close)
        current_close = peak
        current_position = CurrentPosition.PEAK

    return peak, trough, current_close, current_position


    
def find_peak_in_range(q: lq.LinkedQ, current_close: float, lower_level: float, upper_level: float, macro_trend: Trend, allow_immediate_countertrend: bool):

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------





def find_trough_in_range(q: lq.LinkedQ, current_close: float, lower_level: float, upper_level: float, macro_trend: Trend, allow_immediate_countertrend: bool):

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        

def find_initial_breakthrough(q: lq.LinkedQ, lower_level: float, upper_level, current_close: float, current_position: CurrentPosition):
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------  


def find_uptrend_breakthrough(q: lq.LinkedQ, lower_level: float, upper_level, current_close: float, macro_trend: Trend):

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------



def find_up_to_sideways_breakthrough(q: lq.LinkedQ, lower_level: float, upper_level, current_close: float, macro_trend: Trend):

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------

def find_down_to_side_way_breakthrough(q: lq.LinkedQ, lower_level: float, upper_level, current_close: float, macro_trend: Trend):

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    

def find_from_peak_side_to_side_breakthrough(q: lq.LinkedQ, lower_level: float, upper_level, current_close: float, macro_trend: Trend):
    
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------

def find_from_trough_side_to_side_breakthrough(q: lq.LinkedQ, lower_level: float, upper_level, current_close: float, macro_trend: Trend):
    
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------

def find_downtrend_breakthrough(q: lq.LinkedQ, lower_level: float, upper_level, current_close: float, macro_trend: Trend):

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------

def plot_chart(lines, ax, prices: list[float], upper_level: float, lower_level: float, macro_trend: Trend):

    line_stock = lines[0]
    line_upper_level = lines[1]
    line_lower_level = lines[2]

    x = np.arange(len(prices))
    y = prices    
    line_stock.set_xdata(x)
    line_stock.set_ydata(y)

    lower_level_x= [0, len(prices)]
    lower_level_y = [lower_level, lower_level]
    line_lower_level.set_xdata(lower_level_x)
    line_lower_level.set_ydata(lower_level_y)

    upper_level_x= [0, len(prices)]
    upper_level_y = [upper_level, upper_level]
    line_upper_level.set_xdata(upper_level_x)
    line_upper_level.set_ydata(upper_level_y)

    ax.relim()  # Recalculate limits
    ax.autoscale_view()  # Autoscale to fit new data
    ax.set_title(f"Macro Trend {macro_trend.name}")
    plt.draw()  # Redraw the figure
    plt.pause(0.3)  # Pause for a short interval        

def get_macro_trend(prices: list, last_candle_open_time: int, timeframe: TimeFrame, debugger: bool=False) -> dict:


    q: lq.LinkedQ = data_to_queue(prices)
    q.debugger = debugger
    q.last_candle_open_time = last_candle_open_time
    q.timeframe = timeframe

    if debugger == True:
        # Initial plot setup
        x = []
        y = []
        plt.ion()  # Turn on interactive mode
        fig, ax = plt.subplots()
        line_stock, = ax.plot(x, y)
        line_upper_level, = ax.plot(x, y)
        line_lower_level, = ax.plot(x, y)
        q.lines = [line_stock, line_upper_level, line_lower_level]
        q.ax = ax


    try:
        upper_level, lower_level, current_close, current_position = get_initial_controlling_highs_and_lows(q)
        lower_level, upper_level, current_close, macro_trend = find_initial_breakthrough(q, lower_level, upper_level, current_close, current_position)
    except QueueIsEmpty as e:
        return
    
    if macro_trend == Trend.UP:
        current_position = CurrentPosition.PEAK
    else:
        current_position = CurrentPosition.TROUGH

    previous_trend = None

    i = 0

    try:
        while True:
            if macro_trend == Trend.UP:

                # ------------------- REDACTED ---------------------
                    # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                        # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------

            elif macro_trend == Trend.SIDEWAYS:

                # ------------------- REDACTED ---------------------
                    # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                        # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------


            elif macro_trend == Trend.DOWN:

                # ------------------- REDACTED ---------------------
                    # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                        # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                    # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------
                # --------------------------------------------------

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------


        
def calculate_macro_trend(# -----------------------------------------) -> Trend:

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------    
    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------

    return macro_trend       



if __name__ == '__main__':

    # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
    # --------------------------------------------------
        # --------------------------------------------------
            # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------



