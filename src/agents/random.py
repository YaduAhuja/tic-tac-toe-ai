from agents.agent import Agent
from environment import Board
from random import randint

class RandomAgent(Agent):
    def selectMove(self, board: Board):
        moves = board.legalMoves()
        idx = randint(0, len(moves) - 1)
        return moves[idx]
        
        