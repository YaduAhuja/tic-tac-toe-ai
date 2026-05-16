from agents import Agent
from environment import Board, Player, Event

class Game():
    def __init__(self, xAgent: Agent, yAgent: Agent, boardSize: int = 3) -> None:
        self.xAgent = xAgent
        self.yAgent = yAgent

        self.board = Board(boardSize)
        self.currentPlayer = Player.O
    
    def _currentAgent(self) -> Agent:
        if self.currentPlayer == Player.X:
            return self.xAgent
        return self.yAgent

    def step(self):
        agent = self._currentAgent()
        move = agent.selectMove(self.board, self.currentPlayer)
        self.board.place(move, self.currentPlayer)
        agent.onEvent(Event.MOVE)

    
    def play(self) -> Player | None:
        while not self.board.isTerminal():
            self.currentPlayer = Player.O if self.currentPlayer == Player.X else Player.X
            # self.board.render()
            self.step()
            
        # self.board.render()
        winner = self.board.winner()
        if winner is None:
            self.xAgent.onEvent(Event.DRAW)
            self.yAgent.onEvent(Event.DRAW)
            # print("Draw")
        else:
            winnerAgent = self.yAgent
            loserAgent = self.xAgent
            if (winner == Player.X):
                winnerAgent = self.xAgent
                loserAgent = self.yAgent

            winnerAgent.onEvent(Event.WIN)
            loserAgent.onEvent(Event.LOSE)

        return winner
