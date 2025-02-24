import numpy as np
import matplotlib.pyplot as plt
from stock_enums import CloserTo, TimeFrame, InsideZone
import requests
import datetime as dt
import pandas as pd
import time
import json
from order_flow.linked_queue import LinkedQ
from order_flow.zone import Zone, ZoneWarehouse
from order_flow.demand import Demand
from order_flow.supply import Supply
from order_flow.candle import Candle
from order_flow.zone_rulebook import ZoneRulebook


def data_to_queue(data: dict, q: LinkedQ) -> LinkedQ:
    for candle in data["candles"]:
        q.enqueue(candle)
    return q


def gap_up_candle(current_candle: Candle, next_candle: Candle):
    if next_candle.low > current_candle.high:
        return True
    else:
        return False

def gap_down_candle(current_candle: Candle, next_candle: Candle):
    if next_candle.high < current_candle.low:
        return True
    else:
        return False

def get_closer_to_data(zones: ZoneWarehouse, closest_demand: Demand, closest_supply: Supply, current_price):

    if not zones.demand or not zones.supply:
        if not zones.demand and zones.supply:
            percentage = get_zone_percentage(current_price, zones.lowest_low, closest_supply.high)
            tooltip = no_demand_tooltip(zones, closest_supply)
            closer_to_data = {"type": CloserTo.ZONES, "value": percentage, "text": f"{percentage}%\n{CloserTo.NO_DEMAND.value}", "tooltip": tooltip, "fresh": True}
        elif zones.demand and not zones.supply:
            percentage  = get_zone_percentage(current_price, closest_demand.low, zones.highest_high)
            tooltip = no_supply_tooltip(zones, closest_demand)
            closer_to_data = {"type": CloserTo.ZONES, "value": percentage, "text": f"{percentage}%\n{CloserTo.NO_SUPPLY.value}", "tooltip": tooltip, "fresh": True}
        else:
            closer_to_data = {"type": CloserTo, "value": CloserTo.NO_ZONES.value, "text": CloserTo.NO_ZONES.value, "fresh": True}
    else:
        tooltip = closer_to_tooltip(closest_demand, closest_supply)
        percentage = get_zone_percentage(current_price, closest_demand.low, closest_supply.high)
        closer_to_data = {"type": CloserTo.ZONES, "value": percentage, "text": f"{percentage}%", "tooltip": tooltip, "data": (closest_demand, closest_supply), "fresh": True}

    return closer_to_data


def get_zone_percentage(current_price: float, demand_low: float, supply_high: float) -> int:

    # ---------- REDACTED -------------------
    # ---------------------------------------
    percentage = (current_price_range / range) * 100
    percentage = round(percentage)
    return percentage    


def get_inside_zone_data(closest_demand: Demand, closest_supply: Supply, price: float):

    inside_zone_val = get_inside_zone_val(closest_demand, closest_supply, price)

    if inside_zone_val == InsideZone.BOTH.value:
        data = (closest_demand, closest_supply)
        # -------------------- REDACTED ------------------------------
        # --------------------------------------------------
    elif inside_zone_val == InsideZone.DEMAND.value:
        data = closest_demand
        # --------------------------------------------------
    elif inside_zone_val == InsideZone.SUPPLY.value:
        data = closest_supply
        # --------------------------------------------------
    else:
        data = None
        tooltip = None

    inside_zone_data = # ------------------------------------
    return inside_zone_data


def get_inside_zone_val(demand: Demand, supply: Supply, price: float):
    if inside_zone(demand, price) and inside_zone(supply, price):
        return InsideZone.BOTH.value
    elif inside_zone(demand, price) and not inside_zone(supply, price):
        return InsideZone.DEMAND.value
    elif inside_zone(supply, price) and not inside_zone(demand, price):
        return InsideZone.SUPPLY.value
    else:
        return InsideZone.NONE.value


def inside_zone(zone: Demand | Supply, price):
    if zone is None:
        return False

    if price <= zone.high and price >= zone.low:
        return True
    else:
        return False


def filter_zones(zones: ZoneWarehouse, rulebook: ZoneRulebook) -> ZoneWarehouse:

    # -----------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------
    return zones


def find_zones(q: LinkedQ, zones: ZoneWarehouse, rulebook: ZoneRulebook, debugger = False):

    current_candle: Candle = q.dequeue()
    # ---------------------------------
    # ---------------------------------
    
    while True:

        # ----------- REDACTED ---------------

        # ----------
            # ------------------------

        # ---------------------------------------------------
            # ---------------------------------------------------
        # ---------------------------------------------------
            # ---------------------------------------------------

        # ---------------------
            # ------------------------
        # ------------------------
            # ------------------------  

        # -----------------
            # ------------------------
            # ------------------------
                # ------------------------
                # ------------------------
                # ------

        # ------------------------
            # ---------

        # ------------------------
            # ------------------------
            # ------------------------

        # --ANALYSE NEXT CANDLE--
        # ------------------------

        # ------------------------
            # ------------

        # ------------------------

        # ------------------------
            # ------------------------
        # ---
            # ------------------------
            # ------------------------

        # ------------------------
            # ------------------------
            # ------------------------------------------------------
                # ------------------------
                # ------------------------
                # ------------------------
                # ------------------------
                # ------------------------
                # ------
        
        # ------------------------
            # ------------------------
            # ------------------------
                # ------------------------
                # ------------------------
                # ------------------------
                # ------------------------
                # ------------------------
                # ----------

        # ------------------------
            # ------------------------
            # --------------------------------------------------
            # ------------------------------------------------
            # ------------------------
                # ------------------------
                # ------------------------
                # ------------------------
            # ------------------------     
                # ------------------------
                # ------------------------
                # ------------------------

            # ------------------------
            # ------------------------
            continue          

        # ------------------------
        continue

    # ------------------------
        # ------------------------
    # ------------------------
        # ------------------------

    return zones


def find_zone_data(candle_data, current_price: float, debugger=False) -> tuple[dict, dict]:

    rulebook = ZoneRulebook()
    zones = ZoneWarehouse(rulebook)

    q = LinkedQ(zones, debugger)
    q = data_to_queue(candle_data, q)

    zones = find_zones(q, zones, rulebook, debugger)

    zones = filter_zones(zones, rulebook)

    # ------------ REDACTED --------------------
        # ---------------------
    # ---------------------
        # ---------------------
    # ---------------------
        # ---------------------
    # ---------------------
        # ---------------------

    # ---------------------
    # ---------------------

    return closer_to_data, inside_zone_data, zones



if __name__ == "__main__":

    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------         

    

def closer_to_tooltip(closest_demand: Demand, closest_supply: Supply) -> str:
    tooltip = (
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------         
    )
    return tooltip

def no_demand_tooltip(zones: ZoneWarehouse, closest_supply: Supply) -> str:
    tooltip = (
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------         
    )
    return tooltip

def no_supply_tooltip(zones: ZoneWarehouse, closest_demand: Demand) -> str:
    tooltip = (
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------
    # --------------------------------------------------         
    )
    return tooltip