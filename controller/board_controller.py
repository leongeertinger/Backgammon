from model.board import Board
from views.board_view import renderBoard

class BoardController:
    def __init__(self):
        self.board = Board()
    def start(self):
        renderBoard(self.board)
        



