class Node:
    def __init__(self, value, next=None):
        """"Skapar en nod med en pekare, next, och ett värde, value"""
        self.value = value
        self.next = next


class LinkedQ:
    def __init__(self):
        self._first = None
        self._last = None
        self.plotted_prices: list = []
        self.fig = None
        self.lines = []
        self.ax = None
        self.debugger = False
        self.last_candle_open_time = None
        self.timeframe = None


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

            self.plotted_prices.append(first)

            if self._first is None:  # Om vi har tagit bort den sista noden i kön sätter vi även last til None
                self._last = None

            return first

    def isEmpty(self):
        """Kollar om listan är tom"""
        return self._first is None
    


