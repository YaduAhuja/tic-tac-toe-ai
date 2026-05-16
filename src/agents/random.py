from environment.types import Event

from .agent import Agent
from environment import Board, Player
from random import randint

class RandomAgent(Agent):
    def selectMove(self, board: Board, player: Player):
        moves = board.legalMoves()
        idx = randint(0, len(moves) - 1)
        return moves[idx]
        
    def onEvent(self, event: Event):
        return super().onEvent(event)

    def backprop(self):
        return super().backprop()
    
    def reset(self):
        return super().reset()