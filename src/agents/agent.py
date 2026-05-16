from abc import ABC, abstractmethod
from environment import Board, Player, Event

class Agent(ABC):
    @abstractmethod
    def selectMove(self, board:Board, player: Player) -> int: 
        pass

    @abstractmethod
    def onEvent(self, event: Event):
        pass

    @abstractmethod
    def backprop(self):
        pass

    @abstractmethod
    def reset(self):
        pass