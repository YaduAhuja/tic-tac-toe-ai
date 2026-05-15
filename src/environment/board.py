from environment.types import Player

class Board:
    EMPTY = 0

    def __init__(self, size = 3) -> None:
        if (size % 2 == 0 or size < 1):
            raise ValueError("Board size must be a positive odd integer")
        self.size = size * size
        self.winPatterns = self._generateWinPatterns(size)
        self.reset()

    def reset(self) -> None:
        self.cells = [self.EMPTY] * self.size

    def isEmptyAt(self, index: int) -> bool:
        return self.cells[index] == self.EMPTY
    
    def place(self, index: int, player: Player) -> None:
        if not self.isEmptyAt(index):
            raise ValueError("Invalid Move")
        
        self.cells[index] = player.value
    
    def legalMoves(self) -> list[int]:
        return [i for i in range(len(self.cells)) if self.cells[i] == self.EMPTY]
    
    def is_full(self) -> bool:
        return self.EMPTY not in self.cells
    
    def winner(self) -> Player | None :
        for pattern in self.winPatterns:
            a, b, c = pattern
            if (self.cells[a] != self.EMPTY and
                self.cells[a] == self.cells[b] and 
                self.cells[b] == self.cells[c]):
                return Player(self.cells[a])
        return None
            
    
    def clone(self) -> Board:
        newBoard = Board()
        newBoard.cells = [i for i in self.cells]
        return newBoard
    
    @staticmethod
    def _generateWinPatterns(size : int) -> list[list[int]]:
        ret = []
        # Horizontal
        for i in range(0, size * size, size):
            ret.append([i + j for j in range(size)])
        
        # Vertical
        for i in range(size):
            ret.append([i + j for j in range(0, size * size, size)])

        # Diagonal
        ret.append([i for i in range(0, size * size, size + 1)])
        ret.append([i for i in range(size * size - size, size - 2, - (size - 1))])

        return ret
    
    def isTerminal(self) -> bool:
        return self.winner() is not None or self.is_full() 

    
    def render(self):
        for row in range(3):
            start = row * 3
            rowVals = []
            for i in range(3):
                cell = self.cells[start + i]
                if cell == self.EMPTY:
                    rowVals.append(".")
                else:
                    rowVals.append(Player(cell).name)
            
            print("|".join(rowVals))
        print()