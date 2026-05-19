from model.player import Player
from model.tile import Tile

class Board:
    def __init__(self) -> None:
        self.board: dict[int, list] = {
                0:[],
                1: [], 2: [], 3: [], 4: [],
                5: [], 6: [], 7: [], 8: [],
                9: [], 10: [], 11: [], 12: [],
                13: [], 14: [], 15: [], 16: [],
                17: [], 18: [], 19: [], 20: [],
                21: [], 22: [], 23: [], 24: [],
                25: []}
        self._populateBoard()
        self.zone: list[list[int]] = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12], 
                    [13, 14, 15, 16, 17, 18], [19, 20, 21, 22, 23, 24]]
    
    def _populateBoard(self) -> None:
        
        startingPositions: dict[int, tuple] = {
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

    def clearBoard(self, board) -> None:
        for pos in range(26):
            board.board[pos].clear()

    def addTile(self, pos: int, tile: Tile) -> None:
        if not (0 <= pos <= 25):
            return None
        tiles = self.getTilesAt(pos)
        if not tiles:
            self.board[pos].append(tile)
        elif tiles[-1].color == tile.color:
            self.board[pos].append(tile)


    def _setupDebugLogicBoard(self, board) -> None:
        self.clearBoard(board)

    def getCurrentPipCount(self) -> tuple[int, int]:
        whitePipCount = 0
        blackPipCount = 0
        for i in self.board:
            for checker in self.board[i]:
                if checker.color == 'white':
                    whitePipCount += i
                elif checker.color == 'black':
                    blackPipCount += 25 - i
        return whitePipCount, blackPipCount


    def moveTile(self, oldPos: int, newPos: int) -> None:
        if not 0 <= oldPos <= 25:
            return
        if not 0 <= newPos <= 25:
            return
        if not self.board[oldPos]:
            return

        self.board[newPos].append(self.board[oldPos].pop())

    def bearOffTile(self, position: int):
        if not self.getTilesAt(position):
            return
        self.board[position].pop()

    def getTilesAt(self, position: int) -> list[Tile]:
        if position not in self.board:
            raise ValueError(f'Invalid position: {position}')
        return self.board[position]

    def getColorsInZone(self, zone: int) -> dict[str, int]:
        
        tileZone = self.zone[zone - 1]
        tiles = {'white': 0, 'black': 0}
        for i in range(tileZone[0], tileZone[-1] + 1):
            for tile in self.board[i]:
                tiles[tile.color] += 1
        return tiles

    def checkBarredCheckers(self, player: Player) -> bool:
        currentPlayer: str = player.color
        if currentPlayer == 'white' and self.getTilesAt(25):
            return True
        elif currentPlayer == 'black' and self.getTilesAt(0):
            return True
        else:
            return False

    def checkForEndgame(self, player: Player) -> bool:
        if self.checkBarredCheckers(player):
            return False
        zoneOne = self.getColorsInZone(1)
        zoneTwo = self.getColorsInZone(2)
        zoneThree = self.getColorsInZone(3)
        zoneFour = self.getColorsInZone(4)
        if player.color == 'white':
            sumOfTiles = zoneTwo['white'] + zoneThree['white'] + zoneFour['white']
            return sumOfTiles == 0
        elif player.color == 'black':
            sumOfTiles = zoneThree['black'] + zoneTwo['black'] + zoneOne['black']
            return sumOfTiles == 0
        return False

    def getWinningPoints(self, winningPlayer: Player, players: dict[str, Player]) -> int:
        winningColor = winningPlayer.color

        opponent = players['black'] if winningColor == 'white' else players['white']
        opponentBar = 25 if opponent.color == 'white' else 0
        barHasCheckers = len(self.getTilesAt(opponentBar)) > 0

        zoneOne = self.getColorsInZone(1)
        zoneFour = self.getColorsInZone(4)
        playersHomeZone = zoneOne if winningColor == 'white' else zoneFour
        
        #Regular win
        if opponent.tilesTakenOut > 0:
            return 1
        #Gammon win.
        elif playersHomeZone[opponent.color] == 0:
            return 2
        #Backgammon win.
        elif playersHomeZone[opponent.color] != 0 or barHasCheckers:
            return 3
        else:
            return 0
    




