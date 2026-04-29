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
        self.zone = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], 
                    [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24]]
    
    def _populateBoard(self) -> None:
        
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

    def clearBoard(self, board):
        for pos in range(26):
            board.board[pos].clear()

    def _setupDebugLogicBoard(self, board):
        self.clearBoard(board)
        board.board[14].append(Tile('white'))
        board.board[13].append(Tile('white'))
        board.board[8].extend(Tile('black') for _ in range(2))
        board.board[7].extend(Tile('black') for _ in range(2))
        board.board[5].extend(Tile('black') for _ in range(2))

    def getCurrentPipCount(self):
        whitePipCount = 0
        blackPipCount = 0
        for i in self.board:
            for checker in self.board[i]:
                if checker.color == 'white':
                    whitePipCount += i
                elif checker.color == 'black':
                    blackPipCount += 25 - i
        return whitePipCount, blackPipCount


    def moveTile(self, oldPos, newPos) -> None:
        if not 0 <= oldPos <= 25:
            return
        if not 0 <= newPos <= 25:
            return
        if not self.board[oldPos]:
            return

        self.board[newPos].append(self.board[oldPos].pop())

    def bearOffTile(self, position):
        if not self.getTilesAt(position):
            return
        self.board[position].pop()

    def getTilesAt(self, position) -> list[Tile]:
        if position not in self.board:
            raise ValueError(f'Invalid position: {position}')
        return self.board[position]

    def getColorsInZone(self, zone) -> dict[str, int]:
        
        tileZone = self.zone[zone - 1]
        tiles = {'white': 0, 'black': 0}
        for i in range(tileZone[0], tileZone[-1] + 1):
            for tile in self.board[i]:
                tiles[tile.color] += 1
        return tiles

    def checkBarredCheckers(self, player):
        player = player.color
        if player == 'white' and self.getTilesAt(25):
            return True
        elif player == 'black' and self.getTilesAt(0):
            return True
        else:
            return False

    def checkGameState(self, player):
        zoneOne = self.getColorsInZone(1)
        zoneFour = self.getColorsInZone(4)
        if player.color == 'white': 
            return zoneOne['white'] + player.tilesTakenOut == 15
        elif player.color == 'black':
            return zoneFour['black'] + player.tilesTakenOut == 15



