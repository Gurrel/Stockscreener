from enum import Enum

class Position(Enum):
    BELOW = "Below"
    ABOVE = "Above"
    NO_DATA = "..."

class TimeFrame(Enum):
    MINUTES = 1
    MIN_5 = 5
    HOUR = "H"
    DAY = "D"
    WEEK = "W"
    MONTH = "M"

class CandleAttribute(Enum):
    OPEN = "o"
    CLOSE = "c"
    HIGH = "h"
    LOW = "l"
    TIME = "t"
    VOLUME = "v"

class Trend(Enum):
    UP = "UP"
    DOWN = "DOWN"
    SIDEWAYS = "SIDE"
    INSIDE = "INSIDE"

class ZoneAttribute(Enum):
    SUPPLY = "Supply"
    DEMAND = "Demand"
    DESTROYED = "Destroyed"


class CloserTo(Enum):
    ZONES = "ZONES"
    NO_SUPPLY = "NO SUPPLY"
    NO_DEMAND = "NO DEMAND"
    NO_ZONES = "NO ZONES"

class PreviousBar(Enum):
    RANGE = "RANGE"
    OUTSIDE = "Outside"
    INSIDE = "Inside"

class InsideZone(Enum):
    DEMAND = "DEMAND"
    SUPPLY = "SUPPLY"
    BOTH = "BOTH"
    NONE = "NONE"
