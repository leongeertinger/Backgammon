from model.board import Board
from views.board_view import renderBoard
from model.dice import throwDice
from controller.input_handler import getKey
from model.doublingcube import DoublingCube
from model.player import Player
import os

#Should use a nicer math solution here.
navigation = {
    24: {"a": 24, "d": 23, "s": 1},
    23: {"a": 24, "d": 22, "s": 2},
    22: {"a": 23, "d": 21, "s": 3},
    21: {"a": 22, "d": 20, "s": 4},
    20: {"a": 21, "d": 19, "s": 5},
    19: {"a": 20, "d": 0, "s": 6},
    0:  {"a": 19, "d": 18, "s": 25},
    18: {"a": 0, "d": 17, "s": 7},
    17: {"a": 18, "d": 16, "s": 8},
    16: {"a": 17, "d": 15, "s": 9},
    15: {"a": 16, "d": 14, "s": 10},
    14: {"a": 15, "d": 13, "s": 11},
    13: {"a": 14, "d": 13, "s": 12},

    1:  {"a": 1, "d": 2, "w": 24},
    2:  {"a": 1, "d": 3, "w": 23},
    3:  {"a": 2, "d": 4, "w": 22},
    4:  {"a": 3, "d": 5, "w": 21},
    5:  {"a": 4, "d": 6, "w": 20},
    6:  {"a": 5, "d": 25, "w": 19},
    25: {"a": 6, "d": 7, "w": 0},
    7:  {"a": 25, "d": 8, "w": 18},
    8:  {"a": 7, "d": 9, "w": 17},
    9:  {"a": 8, "d": 10, "w": 16},
    10: {"a": 9, "d": 11, "w": 15},
    11: {"a": 10, "d": 12, "w": 14},
    12: {"a": 11, "d": 12, "w": 13},
}



class BoardController:
    def __init__(self):
        self.board = Board()
        self.cursorPosition = 1
        self.remainingMoves = list(throwDice())
        self.usedDice = []
        self.lastMoves = []

        self.players = {
                'white': Player('white', -1),
                'black': Player('black', 1)
                }
        self.firstDiceWhite = throwDice()
        self.firstDiceBlack = throwDice()
        
        self.currentPlayer = self.players[
                self._calculateStartingPlayer(self.firstDiceWhite, self.firstDiceBlack)]
        if self.currentPlayer.color == 'white':
            self.currentPlayersBar = 25
        else:
            self.currentPlayersBar = 0
        self.doublingcube = DoublingCube()

        self.winner = ''
        
        self.running = True

    def _clearScreen(self):
        os.system('clear')
    
    def _moveCursor(self, key):
        if key in navigation[self.cursorPosition]:
            self.cursorPosition = navigation[self.cursorPosition][key]
    
    def _calculateStartingPlayer(self, diceWhite, diceBlack):
        return 'white' if (diceWhite[0] + diceWhite[1]) > (diceBlack[0] + diceBlack[1]) else 'black'

    def _endTurn(self):
        if self.currentPlayer.tilesTakenOut == 15:
            self.winner = self.currentPlayer.color
            return
        if self.currentPlayer.color == 'white':
            self.currentPlayer = self.players['black']
            self.currentPlayersBar = 0
        else:
            self.currentPlayer = self.players['white']
            self.currentPlayersBar = 25
        self.lastMoves.clear()
        self.usedDice.clear()
        self.remainingMoves = list(throwDice())

    def _undo(self):
        if not self.lastMoves:
            return

        moveData = self.lastMoves.pop()

        fromPos = moveData['from']
        toPos = moveData['to']
        diceValue = moveData['dice']
        hitData = moveData['hit']

        self.board.moveTile(toPos, fromPos)
        self.remainingMoves.insert(0, diceValue)

        if hitData:
            if hitData['bar'] == 25: #White bar
                self.board.moveTile(25, hitData['position'])
            else:
                self.board.moveTile(0, hitData['position'])

        if self.usedDice:
            self.usedDice.pop()
        

    def _columnBelongsToCurrentPlayer(self, position):
        tiles = self.board.getTilesAt(position)
        if not tiles:
            return False
        return tiles[-1].color == self.currentPlayer.color

    def _getHittableTile(self, position):
        tiles = self.board.getTilesAt(position)
        if len(tiles) == 1 and tiles[-1].color != self.currentPlayer.color:
            return tiles[-1]
        else:
            return None

    def _hitTile(self, position):
        tiles = self.board.getTilesAt(position)
        if not len(tiles) == 1:
            return
        
        hitTile = tiles[-1]
        
        if tiles[-1].color == 'white':
            self.board.moveTile(position, 25)#Send to white bar.
            bar = 25#Used for undo function.
        else:
            self.board.moveTile(position, 0)#Send to black bar.
            bar = 0
        return {
                'tile': hitTile,
                'bar': bar,
                'position': position
                }

    def _checkForBlockedColumn(self, position):
        tiles = self.board.getTilesAt(position)
        
        if len(tiles) > 1 and tiles[-1].color != self.currentPlayer.color:
            return True
        return False

    def _checkValidEndGameMove(self, fromPos, toPos):
        if self.currentPlayer.color == 'white' and toPos > 25:
            for i in range(fromPos - 1, 19 - 1, -1):
                if self._columnBelongsToCurrentPlayer(i):
                    return False
                else:
                    return True
        if self.currentPlayer.color == 'black' and toPos < 0:
            for i in range(fromPos + 1, 6 + 1):
                if self._columnBelongsToCurrentPlayer(i):
                    return False
                else:
                    return True

    def _selectColumn(self):
        if not self.remainingMoves:
            return

        endGame = self.board.checkGameState(self.currentPlayer)

        barredCheckers = self.board.checkBarredCheckers(self.currentPlayer)
        if barredCheckers and self.cursorPosition != self.currentPlayersBar:
            return

        diceValue = self.remainingMoves[0]
        fromPos = self.cursorPosition
        
        if not self._columnBelongsToCurrentPlayer(fromPos):
            return

        toPos = fromPos + (diceValue * self.currentPlayer.direction)
        
        if not endGame and not 1 <= toPos <= 24:
            return
        if self._checkForBlockedColumn(toPos):
            return

        hitData = None
        if self._getHittableTile(toPos):
            hitData = self._hitTile(toPos)
        
        if endGame and (toPos <= 0 or toPos >= 25):
            if self._checkValidEndGameMove(fromPos, toPos, self.currentPlayer):
                self.board.bearOffTile(fromPos)
                self.currentPlayer.tilesTakenOut += 1
            else:
                return
        else: 
            self.board.moveTile(fromPos, toPos)

        moveData = {
                'from': fromPos,
                'to': toPos,
                'dice': diceValue,
                'hit': hitData
                }

        self.usedDice.append(self.remainingMoves.pop(0))
        self.lastMoves.append(moveData)

    def start(self):
        while self.running:
            self._clearScreen()
            renderBoard(self.board, self.players, self.cursorPosition, self.doublingcube, self.remainingMoves, 
                        self.firstDiceWhite, self.firstDiceBlack, self.board.getCurrentPipCount, self.winner)

            key = getKey().lower()
            if key in ('w', 'a', 's', 'd'):
                self._moveCursor(key)
            elif key in ('\r', '\n') and self.remainingMoves:
                self._selectColumn()
            elif key == 'r':
                self.remainingMoves.reverse()
            elif key == 'u':
                self._undo()
            elif key in ('\r', '\n') and not self.remainingMoves:
                self._endTurn()
            elif key in ('\x1B', '\033'):
                self.running = False
        



