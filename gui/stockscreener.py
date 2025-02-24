from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk
import ctypes as ct
import time
from tkextrafont import Font
from gui.tooltip import ToolTip
from stock_enums import *
from api_handler import ApiHandler
from queues import QueueWarehouse
from locks import LockWarehouse
from resources.stock_data_store import StockDataStore

if TYPE_CHECKING:
    from multiprocessing import Queue

class stockScreener:

    def __init__(self, root: tk.Tk, api_key: str):
        
        self.root: tk.Tk = root
        self.root.title("StockScreener")
        self.root.geometry("800x1000")
        self.api_key = api_key

        self.text_color = "white"
        self.header_color = "#161615"
        self.data_cell_color = "#0F0F0F"
        self.green = "#52EE5F"
        self.yellow = "#FFD15D"
        self.gray = "#808080"
        self.red = "#FF4646"
        self.background_color = "#808080"
        self.border_style = None
        self.no_data = "..."

        self.data_storage = StockDataStore()

        dark_title_bar(root)
        self.root.config(bg=self.background_color)
        self.create_widgets()

    @property
    def data_cells(self):
        cells = (
            self.quote_lbl,
            self.trend_daily_lbl,
            self.trend_weekly_lbl,
            self.trend_monthly_lbl,
            self.vwap_daily_lbl,
            self.vwap_weekly_lbl,
            self.vwap_monthly_lbl,
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
            self.ema20_daily_lbl,
            self.ema20_weekly_lbl,
            self.ema20_monthly_lbl,
            self.ema50_daily_lbl,
            self.ema50_weekly_lbl,
            self.ema50_monthly_lbl,
            self.ema200_daily_lbl,
            self.ema200_weekly_lbl,
            self.ema200_monthly_lbl,            
        )
        return cells
    
    @property
    def tooltips(self):
        tips = (
            self.quote_tooltip,
            self.trend_d_tooltip,
            self.trend_w_tooltip,
            self.trend_m_tooltip,
            self.vwap_d_tooltip,
            self.vwap_w_tooltip,
            self.vwap_m_tooltip,
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
            self.ema20_d_tooltip,
            self.ema20_w_tooltip,
            self.ema20_m_tooltip,
            self.ema50_d_tooltip,
            self.ema50_w_tooltip,
            self.ema50_m_tooltip,
            self.ema200_d_tooltip,
            self.ema200_w_tooltip,
            self.ema200_m_tooltip
        )
        return tips


    def create_widgets(self):

        root = self.root

        # Configure row and column weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=2)
        root.grid_rowconfigure(2, weight=2)
        root.grid_rowconfigure(3, weight=3)
        root.grid_rowconfigure(4, weight=3)
        root.grid_rowconfigure(5, weight=3)
        root.grid_rowconfigure(6, weight=3)
        root.grid_rowconfigure(7, weight=3)
        root.grid_rowconfigure(8, weight=3)
        root.grid_rowconfigure(9, weight=3)
        root.grid_rowconfigure(10, weight=3)

        root.grid_columnconfigure(0, weight=2)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)



        text_font = Font(file="fonts/Inconsolata-Regular.ttf", family="Inconsolata", size=18)
        text_font_small = Font(file="fonts/Inconsolata-Regular2.ttf", family="Inconsolata", size=15)
        font_tooltip = Font(file="fonts/Inconsolata-Regular3.ttf", family="Inconsolata", size=12)


        top_navbar = tk.Frame(root, bg="#131313")
        top_navbar.grid(row=0, column=0, sticky="NSEW", columnspan=4)

        # Configure column weights for the frame
        top_navbar.grid_columnconfigure(0, weight=3)  
        top_navbar.grid_columnconfigure(1, weight=2)  
        top_navbar.grid_columnconfigure(2, weight=2)
        top_navbar.grid_columnconfigure(3, weight=10)
        top_navbar.grid_columnconfigure(4, weight=2)
        top_navbar.grid_rowconfigure(0, weight=1)

        self.ticker_lbl = tk.Label(top_navbar, text=self.no_data, bg="#232323", fg=self.text_color, font=text_font)
        self.ticker_lbl.grid(row=0, column=0, sticky="NSEW")

        self.quote_lbl = tk.Label(top_navbar, text=self.no_data, bg=self.header_color, fg=self.text_color, font=text_font)
        self.quote_lbl.grid(row=0, column=1, sticky="NSEW")
        self.quote_tooltip = ToolTip(self.quote_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.glass_icon = tk.PhotoImage(file=r"icons\magnifying-glass.png").subsample(5, 5)
        self.ocr_window_btn = tk.Button(top_navbar, image=self.glass_icon, bg=self.header_color, relief="raised", borderwidth=5)
        self.ocr_window_btn.grid(row=0, column=2, sticky="NSEW")

        self.start_btn = tk.Button(top_navbar, text="Start", bg=self.header_color, fg=self.text_color, font=text_font, relief="raised", borderwidth=5)
        self.start_btn.grid(row=0, column=4, sticky="NSEW")


        inidicator_lbl = tk.Label(root, text="Indicator", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        inidicator_lbl.grid(row=1, column=0, rowspan=2, sticky="NSEW", padx=1, pady=1)

        timeframe_lbl = tk.Label(root, text="Timeframe", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        timeframe_lbl.grid(row=1, column=1, columnspan=3, sticky="NSEW", padx=1, pady=1)

        daily_lbl = tk.Label(root, text="Daily", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        daily_lbl.grid(row=2, column=1, sticky="NSEW", padx=1, pady=1)

        weekly_lbl = tk.Label(root, text="Weekly", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        weekly_lbl.grid(row=2, column=2, sticky="NSEW", padx=1, pady=1)

        monthly_lbl = tk.Label(root, text="Monthly", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        monthly_lbl.grid(row=2, column=3, sticky="NSEW", padx=1, pady=1)


        trend_lbl = tk.Label(root, text="Trend", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        trend_lbl.grid(row=3, column=0, sticky="NSEW", padx=1, pady=1)

        self.trend_daily_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.trend_daily_lbl.grid(row=3, column=1, sticky="NSEW", padx=1, pady=1)
        self.trend_d_tooltip = ToolTip(self.trend_daily_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.trend_weekly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.trend_weekly_lbl.grid(row=3, column=2, sticky="NSEW", padx=1, pady=1)
        self.trend_w_tooltip = ToolTip(self.trend_weekly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.trend_monthly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.trend_monthly_lbl.grid(row=3, column=3, sticky="NSEW", padx=1, pady=1)
        self.trend_m_tooltip = ToolTip(self.trend_monthly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        vwap_lbl = tk.Label(root, text="VWAP", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        vwap_lbl.grid(row=4, column=0, sticky="NSEW", padx=1, pady=1)

        self.vwap_daily_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.vwap_daily_lbl.grid(row=4, column=1, sticky="NSEW", padx=1, pady=1)
        self.vwap_d_tooltip = ToolTip(self.vwap_daily_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.vwap_weekly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.vwap_weekly_lbl.grid(row=4, column=2, sticky="NSEW", padx=1, pady=1)
        self.vwap_w_tooltip = ToolTip(self.vwap_weekly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.vwap_monthly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.vwap_monthly_lbl.grid(row=4, column=3, sticky="NSEW", padx=1, pady=1)
        self.vwap_m_tooltip = ToolTip(self.vwap_monthly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.inside_zone_lbl = tk.Label(root, text="Inside zone", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        self.inside_zone_lbl.grid(row=5, column=0, sticky="NSEW", padx=1, pady=1)

        self.inside_zone_daily_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.inside_zone_daily_lbl.grid(row=5, column=1, sticky="NSEW", padx=1, pady=1)
        self.inside_zone_d_tooltip = ToolTip(self.inside_zone_daily_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)
        self.inside_zone_weekly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.inside_zone_weekly_lbl.grid(row=5, column=2, sticky="NSEW", padx=1, pady=1)
        self.inside_zone_w_tooltip = ToolTip(self.inside_zone_weekly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)
        self.inside_zone_monthly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.inside_zone_monthly_lbl.grid(row=5, column=3, sticky="NSEW", padx=1, pady=1)
        self.inside_zone_m_tooltip = ToolTip(self.inside_zone_monthly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        closer_to_lbl = tk.Label(root, text="Closer to", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        closer_to_lbl.grid(row=6, column=0, sticky="NSEW", padx=1, pady=1)

        self.closer_to_daily_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.closer_to_daily_lbl.grid(row=6, column=1, sticky="NSEW", padx=1, pady=1)
        self.closer_to_d_tooltip = ToolTip(self.closer_to_daily_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.closer_to_weekly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.closer_to_weekly_lbl.grid(row=6, column=2, sticky="NSEW", padx=1, pady=1)
        self.closer_to_w_tooltip = ToolTip(self.closer_to_weekly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.closer_to_monthly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.closer_to_monthly_lbl.grid(row=6, column=3, sticky="NSEW", padx=1, pady=1)
        self.closer_to_m_tooltip = ToolTip(self.closer_to_monthly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.previous_bar_lbl = tk.Label(root, text="Previous Bar", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        self.previous_bar_lbl.grid(row=7, column=0, sticky="NSEW", padx=1, pady=1)

        self.prev_daily_bar_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.prev_daily_bar_lbl.grid(row=7, column=1, sticky="NSEW", padx=1, pady=1)
        self.prev_daily_bar_tooltip = ToolTip(self.prev_daily_bar_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.prev_weekly_bar_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.prev_weekly_bar_lbl.grid(row=7, column=2, sticky="NSEW", padx=1, pady=1)
        self.prev_weekly_bar_tooltip = ToolTip(self.prev_weekly_bar_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.prev_monthly_bar_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.prev_monthly_bar_lbl.grid(row=7, column=3, sticky="NSEW", padx=1, pady=1)
        self.prev_monthly_bar_tooltip = ToolTip(self.prev_monthly_bar_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        sma20_lbl = tk.Label(root, text="20 EMA", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        sma20_lbl.grid(row=8, column=0, sticky="NSEW", padx=1, pady=1)

        self.ema20_daily_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema20_daily_lbl.grid(row=8, column=1, sticky="NSEW", padx=1, pady=1)
        self.ema20_d_tooltip = ToolTip(self.ema20_daily_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.ema20_weekly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema20_weekly_lbl.grid(row=8, column=2, sticky="NSEW", padx=1, pady=1)
        self.ema20_w_tooltip = ToolTip(self.ema20_weekly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.ema20_monthly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema20_monthly_lbl.grid(row=8, column=3, sticky="NSEW", padx=1, pady=1)
        self.ema20_m_tooltip = ToolTip(self.ema20_monthly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)


        ema50_lbl = tk.Label(root, text="50 EMA", bg=self.header_color, fg=self.text_color, font=text_font, relief=self.border_style)
        ema50_lbl.grid(row=9, column=0, sticky="NSEW", padx=1, pady=1)

        self.ema50_daily_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema50_daily_lbl.grid(row=9, column=1, sticky="NSEW", padx=1, pady=1)
        self.ema50_d_tooltip = ToolTip(self.ema50_daily_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.ema50_weekly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema50_weekly_lbl.grid(row=9, column=2, sticky="NSEW", padx=1, pady=1)
        self.ema50_w_tooltip = ToolTip(self.ema50_weekly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.ema50_monthly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema50_monthly_lbl.grid(row=9, column=3, sticky="NSEW", padx=1, pady=1)
        self.ema50_m_tooltip = ToolTip(self.ema50_monthly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)


        ema200_lbl = tk.Label(root, text="200 EMA", bg=self.header_color, fg=self.text_color, font=text_font)
        ema200_lbl.grid(row=10, column=0, sticky="NSEW", padx=1, pady=1)

        self.ema200_daily_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema200_daily_lbl.grid(row=10, column=1, sticky="NSEW", padx=1, pady=1)
        self.ema200_d_tooltip = ToolTip(self.ema200_daily_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.ema200_weekly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema200_weekly_lbl.grid(row=10, column=2, sticky="NSEW", padx=1, pady=1)
        self.ema200_w_tooltip = ToolTip(self.ema200_weekly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)

        self.ema200_monthly_lbl = tk.Label(root, text=self.no_data, bg=self.data_cell_color, fg=self.gray, font=text_font_small, relief=self.border_style)
        self.ema200_monthly_lbl.grid(row=10, column=3, sticky="NSEW", padx=1, pady=1)
        self.ema200_m_tooltip = ToolTip(self.ema200_monthly_lbl, self.no_data, self.data_cell_color, self.text_color, font_tooltip)    


    def widgets_to_loading_state(self):
        for widget in self.data_cells:
            widget.config(text=Position.NO_DATA.value, fg=self.gray)


    def get_cell_text_color(self, data: dict) -> str:

        value: str = data.get("value")
        text = data.get("text")
        type = data.get("type")

        if value == Position.ABOVE.value or value == Trend.UP.value or value == InsideZone.DEMAND.value:
            return self.green
        elif value == Position.BELOW.value or value == Trend.DOWN.value or value == InsideZone.SUPPLY.value:
            return self.red
        elif value == Trend.SIDEWAYS.value:
            return self.yellow
        elif value == CloserTo.NO_DEMAND.value:
            return self.red
        elif value == CloserTo.NO_SUPPLY.value:
            return self.green
        elif type == CloserTo.ZONES:
            percentage_val = value
            return get_percentage_gradient_color(percentage_val, self.green, self.red)
        elif type == PreviousBar.RANGE:
            percentage_val = value
            return get_previous_bar_data_color(percentage_val, self.yellow, self.green, self.red)
        elif type == "vwap":
            return get_vwap_color(value, self.green, self.red, self.yellow)
        elif value == self.no_data:
            return self.gray
        elif type == "quote":
            return self.text_color
        else:
            return self.gray


    def update(self, queues: QueueWarehouse, locks: LockWarehouse, api_handler: ApiHandler,):

        with locks.ticker:
            self.ticker_lbl.config(text=api_handler.ticker)    

        self.data_storage.update(queues)

        if not self.data_storage.all_confluence_fresh():
            self.root.after(100, self.update, queues, locks, api_handler)
            return

        self.data_storage.find_confluences()
        self.data_storage.find_vwap_trend_confluences()



        for i, data in enumerate(self.data_storage.in_order):
            if data.get("fresh") is True:
                text = data["text"]
                cell = self.data_cells[i]
                cell.config(text=text, fg=self.get_cell_text_color(data))
                tooltip: ToolTip = self.tooltips[i]
                tooltip.text = data.get("tooltip")
                data["fresh"] = False                 

        self.root.after(100, self.update, queues, locks, api_handler)



    def update_data_cells(self, data_store: StockDataStore, api_handler: ApiHandler, locks: LockWarehouse):
        with locks.ticker:
            self.ticker_lbl.config(text=api_handler.ticker)

        for i, data in enumerate(data_store.in_order):
            if data.get("fresh") is True:
                text = data["value"]
                cell = self.data_cells[i]
                cell.config(text=text, fg=self.get_cell_text_color(data))
                tooltip: ToolTip = self.tooltips[i]
                tooltip.text = data.get("tooltip")
                data["fresh"] = False                


def get_vwap_color(percent_val: int, green: str, red: str, yellow: str):
    if percent_val >= 10:
        return green
    elif percent_val <= -10:
        return red
    else:
        return yellow

def get_vwap_percentage_color(data: dict, green: str, red: str):

    trend = data["trend"]
    percent_val = data["value"]
    green_rgb = hex_to_rgb(green)
    red_rgb= hex_to_rgb(red)
    percent_ceiling = 300 # 3 Std deviations

    if trend == Trend.UP.value:
        if percent_val >= 0:
            # Clamp the percentage value between 0 and 200
            percent_val = max(0, min(percent_val, percent_ceiling))
            ratio = percent_val / percent_ceiling
            
        elif percent_val < 0:
            # Clamp the percentage value between -200 and 0
            percent_val = min(0, max(percent_val, -percent_ceiling))            
            ratio = min(percent_val / (-percent_ceiling/8), 1)
            
        gradient_rgb = tuple(
            int(green_rgb[i] + ratio * (red_rgb[i] - green_rgb[i]))
            for i in range(3)
        )
    elif trend == Trend.DOWN.value:
        if percent_val >= 0:
            # Clamp the percentage value between 0 and 200
            percent_val = max(0, min(percent_val, percent_ceiling))
            ratio = min(percent_val / (percent_ceiling/8), 1)
        elif percent_val < 0:
            # Clamp the percentage value between -200 and 0
            percent_val = min(0, max(percent_val, -percent_ceiling))
            ratio = percent_val / (-percent_ceiling)
        gradient_rgb = tuple(
            int(red_rgb[i] + ratio * (green_rgb[i] - red_rgb[i]))
            for i in range(3)
        )        

    elif trend == Trend.SIDEWAYS.value:
        if percent_val >= 0:
            percent_val = max(0, min(percent_val, percent_ceiling))
            ratio = percent_val / percent_ceiling
            gradient_rgb = tuple(
                int(green_rgb[i] + ratio * (red_rgb[i] - green_rgb[i]))
                for i in range(3)
            )
        elif percent_val < 0:
            percent_val = min(0, max(percent_val, -percent_ceiling))
            ratio = percent_val / (-percent_ceiling)
            gradient_rgb = tuple(
                int(red_rgb[i] + ratio * (green_rgb[i] - red_rgb[i]))
                for i in range(3)
            )

    return rgb_to_hex(gradient_rgb)


def get_previous_bar_data_color(percent_val: int, yellow: str, green: str, red: str):
    if percent_val > 110:
        return green
    elif percent_val < -110:
        return red
    else:
        return yellow


def get_percentage_gradient_color(percentage_val: int, low_val_color: str, high_val_color: str):
    """The color parameters should be inputed in HEX"""

    # Clamp the percentage value between 0 and 100
    percentage_val = max(0, min(percentage_val, 100))

    low_val_color_rgb = hex_to_rgb(low_val_color)
    high_val_color_rgb = hex_to_rgb(high_val_color)

    ratio = percentage_val / 100

    gradient_rgb = tuple(
        int(low_val_color_rgb[i] + ratio * (high_val_color_rgb[i] - low_val_color_rgb[i]))
        for i in range(3)
    )

    return rgb_to_hex(gradient_rgb)


@staticmethod
def hex_to_rgb(hex_color: str):
    # Remove the '#' if present and convert each pair of hex digits to an integer.
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

@staticmethod
def rgb_to_hex(rgb: tuple):
    # Format the RGB tuple as a hex string.
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

def dark_title_bar(window):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))
