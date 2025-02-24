from __future__ import annotations
from order_flow.chart_handler import ChartHandler

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from order_flow.zone import Zone, ZoneWarehouse
    from order_flow.demand import Demand
    from order_flow.supply import Supply
    from order_flow.candle import Candle

class Node:
    def __init__(self, value, next=None):
        """"Skapar en nod med en pekare, next, och ett värde, value"""
        self.value = value
        self.next = next


class LinkedQ:
    def __init__(self, zones: ZoneWarehouse, debugger = False):
        self._first = None
        self._last = None
        self.dequeued_candles: list[Candle] = []
        self.debugger = debugger
        self.keybind = ""
        self.zones = zones
        self.dequeue_count = 0
        if self.debugger is True:
            self.chart_handler = ChartHandler()

    def __str__(self):
        """Används för att kunna printa den nya ordningen på korten"""
        elements = []
        first = self._first  # Sparar i en variabel för att inte ändra i kön
        while first is not None:
            elements.append(str(first.value))  # Lägger till values för alla noder i en lista
            first = first.next
        if elements:
            return " ".join(elements)
        else:
            return None

    def peek(self):
        if self._first != None:
            return self._first.value


    def one_left(self):
        if self._first != None:
            if self._first.next is None:
                return True
        return False


    def enqueue(self, value):
        """Skapar ny nod och lägger den sist i kön"""
        new = Node(value)
        if self._first is None:  # Om listan är tom blir den nya noden både först och sist i kön
            self._first = new
            self._last = new
        else:
            self._last.next = new  # Noden som var sist innan pekar på den nya noden
            self._last = new  # Den nya noden är sist i kön
        

    def dequeue(self):
        """Tar bort den första noden i kön"""

        if self._first is None:
            return None
        
        if self._first is not None:
            
            first = self._first.value  # Sparar värdet av första noden för att kuna returna det senare
            self._first = self._first.next  # Sätter first pointern till den andra noden i kön

            self.dequeued_candles.append(first)
            self.dequeue_count += 1

            if self.debugger is True:
                self.chart_handler.update_chart(self.dequeued_candles, self.dequeue_count, self.zones)

            if self._first is None:  # Om vi har tagit bort den sista noden i kön sätter vi även last til None
                self._last = None

            if self.debugger is True:
                self.keybind = input().strip()
                if self.keybind == "#":
                    raise KeyboardInterrupt

            return first
        
    def clone(self, debugger: bool):

        new_queue = LinkedQ(self.zones, debugger)
        new_queue.dequeued_candles = self.dequeued_candles.copy()
        new_queue.dequeue_count = self.dequeue_count

        current = self._first
        while current is not None:
            new_queue.enqueue(current.value)
            current = current.next
        return new_queue
        

    def __len__(self) -> int:

        length = 0
        first = self._first
        while first is not None:
            first = first.next
            length += 1

        return length

    def isEmpty(self):
        """Kollar om listan är tom"""
        return self._first is None
