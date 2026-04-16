from model.tile import Tile

class Board:
    def __init__(self):
        self.board = {
                0:[],
                1: [], 2: [], 3: [], 4: [],
                5: [], 6: [], 7: [], 8: [],
                9: [], 10: [], 11: [], 12: [],
                13: [], 14: [], 15: [], 16: [],
                17: [], 18: [], 19: [], 20: [],
                21: [], 22: [], 23: [], 24: [],
                25: []}
        self._populateBoard()
    
    def _populateBoard(self):
        
        startingPositions = {
                1: ('black', 2),
                6: ('white', 5),
                8: ('white', 3),
                12: ('black', 5),
                13: ('white', 5),
                17: ('black', 3),
                19: ('black', 5),
                24: ('white', 2)
                }
        for position, (color, amount) in startingPositions.items():
            self.board[position].extend(Tile(color) for _ in range(amount))

    def moveTile(self, oldPos, newPos):
        if not 0 <= newPos <= 25:
            return
        self.board[newPos].append(self.board[oldPos].pop())

    def getTilesAt(self, position) -> list[object]:
        if position not in self.board:
            raise ValueError(f'Invalid position: {position}')
        return self.board[position]
