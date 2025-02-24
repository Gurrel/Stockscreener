from __future__ import annotations
from typing import TYPE_CHECKING
import time
from stock_enums import TimeFrame

    

class Candle:

    def __init__(self, open: float = None, high: float = None, low: float = None, close: float = None, time: int = None, timeframe: str = None, previous_candle = None):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.time = time
        self.timeframe = timeframe
        self.closed = True
        self.previous_candle = previous_candle
        # -------------- REDACTED ---------------


    def is_green_candle(self) -> bool:
        if self.close > self.open:
            return True
        else:
            return False
    

    def is_red_candle(self) -> bool:
        if self.close < self.open:
            return True
        else:
            return False

    def #-------------------
        # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------

    def # -----------------
        # ------------------- REDACTED ---------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        
    def is_gap_up_candle(self):

        if self.previous_candle is None:
            return False

        if self.low > self.previous_candle.high:
            return True
        else:
            return False

    def is_gap_down_candle(self):

        if self.previous_candle is None:
            return False

        if self.high < self.previous_candle.low:
            return True
        else:
            return False
        
    def is_closed(self):
        from api_handler import get_market_day_close_unix_time, get_market_week_close_unix_time, get_market_month_close_unix_time
        if self.timeframe == TimeFrame.DAY.name:
            closing_time = get_market_day_close_unix_time(self.time)
        elif self.timeframe == TimeFrame.WEEK.name:
            closing_time = get_market_week_close_unix_time(self.time)
        elif self.timeframe == TimeFrame.MONTH.name:
            closing_time = get_market_month_close_unix_time(self.time)

        current_unix_time = int(time.time())    
        if current_unix_time < closing_time:
            self.closed = False
            return False
        else:
            self.closed = True
            return True

    def # ----------------------------------------
        # ------------------- REDACTED ---------------------
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


    def __str__(self):
        return f"(o: {self.open}, h: {self.high}, l: {self.low}, c: {self.close})"