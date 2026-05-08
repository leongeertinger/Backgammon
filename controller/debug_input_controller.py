from model.tile import Tile

class DebugController:
    def __init__(self, boardController) -> None:
        self.currentlyPlacingTile = 'white'
        self.boardController = boardController
    def handleDebugInput(self, key: str):    
        if key =="1":
            self.currentlyPlacingTile = 'white' 
        elif key == "2":
            self.currentlyPlacingTile = 'black'
        elif key == "3":
            if not self.boardController.remainingMoves:
                self.boardController.remainingMoves.extend([1, 1])
            else:
                currentDice = self.boardController.remainingMoves[0]
                self.boardController.remainingMoves[0] = (1 + currentDice % 6)
        elif key == "4":
            if not self.boardController.remainingMoves:
                self.boardController.remainingMoves.extend([1, 1])
            elif len(self.boardController.remainingMoves) == 1:
                self.boardController.remainingMoves.append(1)
            else:
                currentDice = self.boardController.remainingMoves[1]
                self.boardController.remainingMoves[1] = (1 + currentDice % 6)
        elif key in ("\r" or "\n"):
            tile = Tile('white') if self.currentlyPlacingTile == 'white' else Tile('black')
            self.boardController.board.addTile(self.boardController.cursorPosition, tile)
        elif key == 'c':
            self.boardController.board.clearBoard(self.boardController.board)
        elif key == "x":
            self.boardController.debug = False
