from enum import Enum

class Actions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    PICKUP = 5
    DROPOFF = 6

class ExplorationMethod(Enum):
    PRANDOM = 1
    PEXPLOIT = 2
    PGREED = 3