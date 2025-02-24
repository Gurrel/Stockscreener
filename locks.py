class LockWarehouse:

    def __init__(self, manager):

        self.ticker = manager.Lock()
        self.minute_data = manager.Lock()
        self.min5_data = manager.Lock()
        self.daily_data = manager.Lock()
        self.weekly_data = manager.Lock()
        self.monthly_data = manager.Lock()
        self.latest_price = manager.Lock()
        self.latest_quote = manager.Lock()
        
        self.vwap = manager.Lock()