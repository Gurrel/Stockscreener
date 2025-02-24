from multiprocessing import Queue

class QueueWarehouse:

    def __init__(self):
        self.ticker = Queue()
        self.quote_price = Queue()
        self.trend_d = Queue()
        self.trend_w = Queue()
        self.trend_m = Queue()
        self.vwap_d = Queue()
        self.vwap_w = Queue()
        self.vwap_m = Queue()
        self.inside_zone_d = Queue()
        self.inside_zone_w = Queue()
        self.inside_zone_m = Queue()
        self.closer_to_d = Queue()
        self.closer_to_w = Queue()
        self.closer_to_m = Queue()
        self.prev_bar_d = Queue()
        self.prev_bar_w = Queue()
        self.prev_bar_m = Queue()
        self.sma20_d = Queue()
        self.sma20_w = Queue()
        self.sma20_m = Queue()
        self.sma50_d = Queue()
        self.sma50_w = Queue()
        self.sma50_m = Queue()
        self.sma200_d = Queue()
        self.sma200_w = Queue()
        self.sma200_m = Queue()

        self.ticker_region = Queue()
        self.zones_d = Queue()
        self.zones_w = Queue()
        self.zones_m = Queue()

    @property
    def queues_in_order(self):
        return(
            self.quote_price,
            self.trend_d,
            self.trend_w,
            self.trend_m,
            self.vwap_d,
            self.vwap_w,
            self.vwap_m,
            self.inside_zone_d,
            self.inside_zone_w,
            self.inside_zone_m,
            self.closer_to_d,
            self.closer_to_w,
            self.closer_to_m,
            self.prev_bar_d,
            self.prev_bar_w,
            self.prev_bar_m,
            self.sma20_d,
            self.sma20_w,
            self.sma20_m,
            self.sma50_d,
            self.sma50_w,
            self.sma50_m,
            self.sma200_d,
            self.sma200_w,
            self.sma200_m,
            self.zones_d,
            self.zones_w,
            self.zones_m,
        )