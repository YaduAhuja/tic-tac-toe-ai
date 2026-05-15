from environment import Board
from agents import RandomAgent
from game import Game

xAgent = RandomAgent()
yAgent = RandomAgent()

game = Game(xAgent, yAgent)
game.play()