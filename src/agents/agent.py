from abc import ABC, abstractmethod
from environment import Board

class Agent(ABC):
    @abstractmethod
    def selectMove(self, board:Board) -> int: 
        pass