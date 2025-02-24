from __future__ import annotations
import matplotlib.pyplot as plt
import matplotlib.patches as patches


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from order_flow.zone import Zone, ZoneWarehouse
    from order_flow.demand import Demand
    from order_flow.supply import Supply
    from order_flow.candle import Candle
    from stock_enums import CandleAttribute, ZoneAttribute

class ChartHandler:
    def __init__(self):
        self.initialize_chart()
    
    def initialize_chart(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()

        self.ax.set_title("Chart Plot")
        self.ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        self.ax.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
        self.demand_rects: dict[Demand] = {}
        self.supply_rects: dict[Supply] = {}
    
    def update_chart(self, dequeued_candles: list[Candle], dequeue_count: int, zones: ZoneWarehouse):
        indexes = range(len(dequeued_candles))

        body_width = 0.9
        wick_width = 0.11

        # Remove old bars (except demand zone rectangles)
        for bar in self.ax.patches[:]:  
            if bar.get_alpha() != 0.5:  
                bar.remove()

        for price_idx in indexes:
            open = dequeued_candles[price_idx].open
            high = dequeued_candles[price_idx].high
            low = dequeued_candles[price_idx].low
            close = dequeued_candles[price_idx].close

            body_color = "green" if green_candle(open=open, close=close) else "red"

            # Wick
            self.ax.bar(price_idx, high - max(open, close), wick_width, bottom=max(open, close), color="black")
            self.ax.bar(price_idx, min(open, close) - low, wick_width, bottom=low, color="black")

            # Body
            self.ax.bar(price_idx, abs(close - open), body_width, bottom=min(open, close), color=body_color)

        for demand in list(self.demand_rects.keys()):  # Iterate over a copy to avoid modification issues
            if demand not in zones.demand:  # Check if demand was removed
                self.demand_rects[demand].remove()  # Remove the rectangle from the plot
                del self.demand_rects[demand]  # Remove from the dictionary

        for demand in zones.demand:
            x, y = demand.x, demand.low
            width = dequeue_count - x + 2
            height = demand.height

            if demand not in self.demand_rects:
                rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor="black", facecolor='limegreen', alpha=0.5)
                demand.rect = rect
                self.ax.add_patch(rect)
                self.demand_rects[demand] = rect
            else:
                self.demand_rects[demand].set_width(width)


        for supply in list(self.supply_rects.keys()):
            if supply not in zones.supply:
                self.supply_rects[supply].remove()
                del self.supply_rects[supply]

        for supply in zones.supply:
            x, y = supply.x, supply.low
            width = dequeue_count - x + 2
            height = supply.height

            if supply not in self.supply_rects:
                rect = patches.Rectangle((x, y), width, height, linewidth=1, edgecolor="black", facecolor='indianred', alpha=0.5)
                supply.rect = rect
                self.ax.add_patch(rect)
                self.supply_rects[supply] = rect
            else:
                self.supply_rects[supply].set_width(width)

        # Reduce expensive autoscaling
        if len(dequeued_candles) < 30:
            self.ax.relim()
            self.ax.autoscale_view()

        self.fig.canvas.draw_idle()  # Faster refresh
        self.fig.canvas.flush_events()  # Ensures UI updates
        plt.pause(0.3)


def green_candle(candle: CandleAttribute = None, open: float = None, close: float = None):

    if candle != None:
        close = candle.close
        open = candle.open

    if (close - open) >= 0:
        return True
    else:
        return False