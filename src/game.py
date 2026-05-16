from agents import Agent
from environment import Board, Player

class Game():
    def __init__(self, xAgent: Agent, yAgent: Agent, boardSize: int = 3) -> None:
        self.xAgent = xAgent
        self.yAgent = yAgent

        self.board = Board(boardSize)
        self.currentPlayer = Player.X
    
    def _currentAgent(self) -> Agent:
        if self.currentPlayer == Player.X:
            return self.xAgent
        return self.yAgent

    def step(self):
        agent = self._currentAgent()
        move = agent.selectMove(self.board)
        self.board.place(move, self.currentPlayer)
        self.currentPlayer = Player.O if self.currentPlayer == Player.X else Player.X

    
    def play(self):
        while not self.board.isTerminal():
            self.board.render()
            self.step()

        self.board.render()
        winner = self.board.winner()
        if winner is None:
            print("Draw")
        else:
            print(f"Winner: {winner.name}")
