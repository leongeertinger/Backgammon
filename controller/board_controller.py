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
    19: {"a": 20, "d": 18, "s": 6},
    18: {"a": 19, "d": 17, "s": 7},
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
    6:  {"a": 5, "d": 7, "w": 19},
    7:  {"a": 6, "d": 8, "w": 18},
    8:  {"a": 7, "d": 9, "w": 17},
    9:  {"a": 8, "d": 10, "w": 16},
    10: {"a": 9, "d": 11, "w": 15},
    11: {"a": 10, "d": 12, "w": 14},
    12: {"a": 11, "d": 12, "w": 13},
}

def _calculateStartingPlayer(diceWhite, diceBlack):
    return 'white' if (diceWhite[0] + diceWhite[1]) > (diceBlack[0] + diceBlack[1]) else 'black'

class BoardController:
    def __init__(self):
        self.board = Board()
        self.cursorPosition = 1
        self.remainingMoves = list(throwDice())

        self.players = {
                'white': Player('white', -1),
                'black': Player('black', 1)
                }
        self.firstDiceWhite = throwDice()
        self.firstDiceBlack = throwDice()
        
        self.currentPlayer = self.players[
                self._calculateStartingPlayer(self.firstDiceWhite, self.firstDiceBlack)]

        self.doublingcube = DoublingCube()
        
        self.running = True

    def _clearScreen(self):
        os.system('clear')
    
    def _moveCursor(self, key):
        if key in navigation[self.cursorPosition]:
            self.cursorPosition = navigation[self.cursorPosition][key]
    
    def _calculateStartingPlayer(self, diceWhite, diceBlack):
        return 'white' if (diceWhite[0] + diceWhite[1]) > (diceBlack[0] + diceBlack[1]) else 'black'

    def _switchPlayer(self):
        if self.currentPlayer.color == 'white':
            self.currentPlayer = self.players['black']
        else:
            self.currentPlayer = self.players['white']

    def _endOrContinueTurn(self):
        self._switchPlayer()
        self.dice = throwDice()

    def _columnBelongsToCurrentPlayer(self, position):
        tiles = self.board.getTilesAt(position)
        if not tiles:
            return False
        return tiles[0].color == self.currentPlayer.color

    def _selectColumn(self):
        if not self.remainingMoves:
            return

        steps = self.remainingMoves[0]
        fromPos = self.cursorPosition
        
        if not self._columnBelongsToCurrentPlayer(fromPos):
            return

        toPos = fromPos + (steps * self.currentPlayer.direction)

        if 1 > toPos > 24:
            return

        self.board.moveTile(fromPos, toPos)
        self.remainingMoves.pop(0)

    def start(self):
        while self.running:
            self._clearScreen()
            renderBoard(self.board, self.cursorPosition, self.remainingMoves, self.firstDiceWhite, self.firstDiceBlack)

            key = getKey()
            if key in ('w', 'a', 's', 'd'):
                self._moveCursor(key)
            elif key in ('\r', '\n') and self.remainingMoves:
                self._selectColumn()
            elif key in ('\r', '\n') and not self.remainingMoves:
                self._switchPlayer()
                self.remainingMoves = list(throwDice())
            elif key in ('\x1B', '\033'):
                self.running = False
        



