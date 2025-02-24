from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from order_flow.demand import Demand
    from order_flow.supply import Supply
    from order_flow.candle import Candle
    from order_flow.zone_rulebook import ZoneRulebook
    

class ZoneWarehouse:

    def __init__(self, rulebook: ZoneRulebook):
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------      
        self.rulebook = rulebook


    def remove_intersecting_demand(self, new_demand: Demand):

        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
  

    def remove_intersecting_supply(self, new_supply: Supply):

        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------

    def remove_destroyed_zones(self, current_candle: Candle):

        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------








class Zone:

    def __init__(self, candle: Candle):
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------

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
        
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
        # --------------------------------------------------
    
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


