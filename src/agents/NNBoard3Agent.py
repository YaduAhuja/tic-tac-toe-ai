from torch import nn, Tensor, distributions, optim
import torch
from .agent import Agent
from environment import Board, Player, Event
import os

class NNBoard3Agent(nn.Module, Agent):
    def __init__(self, learning = True) -> None:
        super().__init__()
        self.learning = learning
        self.model = nn.Sequential(
            nn.Linear(9, 24),
            nn.ReLU(),
            nn.Linear(24, 24),
            nn.ReLU(),
            nn.Linear(24, 9)
        )
        self.optimizer = optim.Adam(self.model.parameters())
        self.states: list[Tensor] = []
        self.actions: list[Tensor] = []
        self.logProbs: list[Tensor] = []
        self.rewards: list[int] = []

    def forward(self, x):
        return self.model(x)

    def selectMove(self, board: Board, player: Player) -> int:
        tensor = self._preprocessBoardState(board, player)
        self.states.append(tensor)
        logits = self(tensor)
        mask = torch.full((9,), float("-inf"))
        legalMoves = board.legalMoves()
        for m in legalMoves:
            mask[m] = 0.0
        
        maskedLogits = logits + mask
        dist = distributions.Categorical(logits=maskedLogits)
        if self.learning:
            action = dist.sample()
        else:
            action = torch.argmax(dist.probs)
        self.actions.append(action)
        self.logProbs.append(dist.log_prob(action))
        return action.item().__int__()
    
    def onEvent(self, event: Event):
        if event == Event.MOVE:
            self.rewards.append(-2)
        else:
            diff = 0
            if event == Event.DRAW:
                diff = 50
            elif event == Event.LOSE:
                diff = -100
            elif event == Event.WIN:
                diff = 100
            self.rewards[-1] += diff

    def reset(self):
        self.states = []
        self.actions = []
        self.logProbs = []
        self.rewards = []
    
    def backprop(self):
        # Pre Backpropagation
        returns = [x for x in self.rewards]
        for i in range(len(returns) - 2, -1, -1):
            returns[i] += returns[i+1]
        
        logProbsTsr = torch.stack(self.logProbs)
        returnsTsr = torch.tensor(returns, dtype=torch.float32)
        loss = - (logProbsTsr * returnsTsr).sum()

        # Backpropagation
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        self.reset()

    def save(self, path:str):
        os.makedirs(path[:path.index("/")], exist_ok=True)
        torch.save(self.model.state_dict(), path)

    @staticmethod
    def load(path: str) -> 'NNBoard3Agent':
        agent = NNBoard3Agent()
        agent.model.load_state_dict(torch.load(path))
        return agent

    @staticmethod
    def _preprocessBoardState(board: Board, player: Player) -> Tensor:
        state = board.state()
        processed = []
        for value in state:
            if value == Board.EMPTY:
                processed.append(value)
            elif value == player.value:
                processed.append(1)
            else:
                processed.append(-1)
        return Tensor(processed)