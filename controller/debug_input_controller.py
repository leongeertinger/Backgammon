from model.tile import Tile

class DebugController:
    def __init__(self, boardController, state) -> None:
        self.state = state

        self.currentlyPlacingTile = 'white'
        self.boardController = boardController
    
    def handleDebugInput(self, key: str) -> None:    
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
            if self.checkForDuplicateDice(self.boardController.remainingMoves):
                self.boardController.remainingMoves = [
                        self.boardController.remainingMoves[0] for _ in range(4)
                        ]
            else:
                self.boardController.remainingMoves = self.boardController.remainingMoves[:2]
        elif key == "4":
            if not self.boardController.remainingMoves:
                self.boardController.remainingMoves.extend([1, 1])
            elif len(self.boardController.remainingMoves) == 1:
                self.boardController.remainingMoves.append(1)
            else:
                currentDice = self.boardController.remainingMoves[1]
                self.boardController.remainingMoves[1] = (1 + currentDice % 6)
            if self.checkForDuplicateDice(self.boardController.remainingMoves):
                self.boardController.remainingMoves = [
                        self.boardController.remainingMoves[0] for _ in range(4)
                        ]
            else:
                self.boardController.remainingMoves = self.boardController.remainingMoves[:2]
                
        elif key == 'f':
            player = self.boardController.currentPlayer
            if player.color == 'white':
                self.boardController.currentPlayer = self.boardController.players['black']
            else:
                self.boardController.currentPlayer = self.boardController.players['white']
        elif key in ("\r", "\n"):
            tiles = self.boardController.board.getTilesAt(self.boardController.cursorPosition)
            if len(tiles) >= 50:
                return
            tile = Tile('white') if self.currentlyPlacingTile == 'white' else Tile('black')
            self.boardController.board.addTile(self.boardController.cursorPosition, tile)
        elif key in ('\b', '\x7f'):
            tiles = self.boardController.board.getTilesAt(self.boardController.cursorPosition)
            if tiles:
                tiles.pop()
        elif key == 'c':
            self.boardController.board.clearBoard(self.boardController.board)
        elif key == "x":
            self.boardController.debug = False
        elif key in ('\x1b', '\033', '\x03'):
            self.state.setState('main-menu')
    
    def checkForDuplicateDice(self, dice: list[int] | list) -> bool:
        if len(dice) >= 2:
            if dice[0] == dice[1]:
                return True
        return False

