from __future__ import annotations
from typing import TYPE_CHECKING
from queues import QueueWarehouse

if TYPE_CHECKING:
    from order_flow.zone import Zone, ZoneWarehouse
    from order_flow.supply import Supply
    from order_flow.demand import Demand
    from gui.stockscreener import stockScreener
    from api_handler import ApiHandler
    from locks import LockWarehouse

class StockDataStore:
    def __init__(self):
        self.quote = {}
        self.trend_daily = {}
        self.trend_weekly = {}
        self.trend_monthly = {}
        self.vwap_daily = {}
        self.vwap_weekly = {}
        self.vwap_monthly = {}
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        self.sma20_daily = {}
        self.sma20_weekly = {}
        self.sma20_monthly = {}
        self.sma50_daily = {}
        self.sma50_weekly = {}
        self.sma50_monthly = {}
        self.sma200_daily = {}
        self.sma200_weekly = {}
        self.sma200_monthly = {}
        self.daily_zones: ZoneWarehouse = None
        self.weekly_zones: ZoneWarehouse = None
        self.monthly_zones: ZoneWarehouse = None

    def update(self, queues: QueueWarehouse):

        attributes = list(vars(self).keys())

        for i, queue in enumerate(queues.queues_in_order):
            if not queue.empty() and i < len(attributes):
                recieved_data = queue.get()
                setattr(self, attributes[i], recieved_data)

    def all_confluence_fresh(self):
        if all(data.get("fresh") for data in self.confluence_data):
            return True
        else:
            return False

    def find_vwap_trend_confluences(self):
        confluences = [(self.vwap_daily, self.trend_daily), (self.vwap_weekly, self.trend_weekly), (self.vwap_monthly, self.trend_monthly)]
        for vwap, trend in confluences:
            vwap["trend"] = trend["value"]

        
    def find_confluences(self):
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
    @property
    def confluence_signals(self):
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
    
    @property
    def confluence_data(self):
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------
        # --------- REDACTED -----------

    @property
    def in_order(self):
        data = [
            self.quote,
            self.trend_daily,
            self.trend_weekly,
            self.trend_monthly,
            self.vwap_daily,
            self.vwap_weekly,
            self.vwap_monthly,
            self.inside_zone_daily,
            self.inside_zone_weekly,
            self.inside_zone_monthly,
            self.closer_to_daily,
            self.closer_to_weekly,
            self.closer_to_monthly,
            self.prev_daily_bar,
            self.prev_weekly_bar,
            self.prev_monthly_bar,
            self.sma20_daily,
            self.sma20_weekly,
            self.sma20_monthly,
            self.sma50_daily,
            self.sma50_weekly,
            self.sma50_monthly,
            self.sma200_daily,
            self.sma200_weekly,
            self.sma200_monthly
        ]
        return data 
 
    