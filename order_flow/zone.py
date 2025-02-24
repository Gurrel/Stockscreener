from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from order_flow.demand import Demand
    from order_flow.supply import Supply
    from order_flow.candle import Candle
    from order_flow.zone_rulebook import ZoneRulebook
    

class ZoneWarehouse:

    def __init__(self, rulebook: ZoneRulebook):
        self.unfinished_zone: Zone = None
        self.supply: list[Supply] = []
        self.demand: list[Demand] = []
        self.highest_high = None
        self.lowest_low = None
        self.rulebook = rulebook


    def remove_intersecting_demand(self, new_demand: Demand):

        self.demand = [demand for demand in self.demand 
                       if (demand.high - new_demand.low) / new_demand.height < self.rulebook.new_intersect_limit
                       and (demand.high - new_demand.low) / demand.height < self.rulebook.old_intersect_limit
                       ]

    def remove_intersecting_supply(self, new_supply: Supply):

        self.supply = [supply for supply in self.supply
                        if (new_supply.high - supply.low) / new_supply.height < self.rulebook.new_intersect_limit
                        and (new_supply.high - supply.low) / new_supply.height < self.rulebook.old_intersect_limit
                       ]

    def remove_destroyed_zones(self, current_candle: Candle):

        self.demand = [demand for demand in self.demand if not demand.destroyed_zone(current_candle.close, current_candle.low)]
        self.supply = [supply for supply in self.supply if not supply.destroyed_zone(current_candle.close, current_candle.high)]








class Zone:

    def __init__(self, candle: Candle):
        self.highest_body = self.get_highest_body(candle.open, candle.close)
        self.highest_wick = candle.high
        self.lowest_wick = candle.low
        self.lowest_body = self.get_lowest_body(candle.open, candle.close)
        self.length = 1 # How many candles the zone is built on

    def get_lowest_body(self, open: float, close: float):
        if open < close:
            return open
        else:
            return close
        
    def get_highest_body(self, open: float, close: float):
        if open > close:
            return open
        else:
            return close

    def update_borders(self, other_zone: Zone):
        if type(other_zone) != Zone:
            print("Error: The other_zone in update_borders() is not a Zone Object")
            return
        
        if other_zone.highest_wick > self.highest_wick:
            self.highest_wick = other_zone.highest_wick
        if other_zone.lowest_wick < self.lowest_wick:
            self.lowest_wick = other_zone.lowest_wick
        if other_zone.highest_body > self.highest_body:
            self.highest_body = other_zone.highest_body
        if other_zone.lowest_body < self.lowest_body:
            self.lowest_body = other_zone.lowest_body

    def increase_length(self):
        self.length += 1

    def valid_supply(self):
        if self.highest_wick - self.lowest_body == 0:
            return False
        return True
    
    def valid_demand(self):
        if self.highest_body - self.lowest_wick == 0:
            return False 
        return True


