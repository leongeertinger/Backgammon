from model.board import Board
from views.board_view import renderBoard
from model.dice import throwDice
from controller.input_handler import getKey
import os

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

class BoardController:
    def __init__(self):
        self.board = Board()
        self.cursorPosition = 1
        self.dice = throwDice()
        self.running = True

    def _clearScreen(self):
        os.system('clear')

    def _moveCursor(self, key):
        if key in navigation[self.cursorPosition]:
            self.cursorPosition = navigation[self.cursorPosition][key]

    def _selectColumn(self):
        steps = self.dice[0]
        fromPos = self.cursorPosition
        toPos = fromPos + steps

        if toPos > 24:
            return

        if not self.board.getTilesAt(fromPos):
            return

        self.board.moveTile(fromPos, toPos)
        self.dice = throwDice()

    def start(self):
        while self.running:
            self._clearScreen()
            renderBoard(self.board, self.cursorPosition, self.dice)

            key = getKey()
            if key in ('w', 'a', 's', 'd'):
                self._moveCursor(key)
            elif key in ('\r', '\n'):
                self._selectColumn()
            elif key in ('\x1B', '\033'):
                self.running = False
        



