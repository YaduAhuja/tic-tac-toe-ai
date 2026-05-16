from enum import Enum

class Player(Enum):
    X = 1
    O = -1

    # @property
    # def symbol(self):
    #     return self.name


class Event(Enum):
    MOVE = "move"
    WIN = "win"
    LOSE = "lose"
    DRAW = "draw"