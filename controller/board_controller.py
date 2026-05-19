from model import player
from model.board import Board
from model.tile import Tile
from views.board_view import renderBoard
from model.dice import throwDice
from controller.input_handler import getKey
from model.doublingcube import DoublingCube
from model.player import Player
from model.navigation import navigation
from controller.debug_input_controller import DebugController
from model.stateManager import StateManager
from model.mainmenu import MainMenu
from controller.mainmenu_controller import MenuController
from views.menu_view import MenuRenderer
from copy import deepcopy
import os

class BoardController:
    def __init__(self) -> None:
        self.state = StateManager()
        
        self.mainmenu = MenuController(MainMenu, self.state)

        self.menuRenderer = MenuRenderer()

        self.firstToWins: int = 1
        self.gameWon = False

        self.board: Board = Board()
        self.cursorPosition: int = 1
        self.remainingMoves: list[int] = []
        self.usedDice: list[int] = []
        self.lastMoves: list[dict] = []

        self.players: dict[str, Player] = {
                'white': Player('white', -1),
                'black': Player('black', 1)
                }
        self.firstDiceWhite: int | None = None
        self.firstDiceBlack: int | None = None
        
        self.currentPlayer: Player | None = None
        self.doublingcube: DoublingCube = DoublingCube() #Not implemented yet

        self.debug = False
        self.debugSetupDone = False
        self.startingRound = True
        self.debugInputController = DebugController(self, self.state)
    
    def _resetController(self, board: Board) -> None:#Has no use yet
        """Resets controller so a new game can be started."""
        board.clearBoard(board)
        board._populateBoard()
        self.usedDice = []
        self.lastMoves = []
        self.remainingMoves = []
        self.firstDiceWhite = None
        self.firstDiceBlack = None
        self.startingRound = True
        self.currentPlayer = None


    def _requirePlayer(self) -> Player:
        """Guarantees that currentPlayer is not None during runtime"""
        if self.currentPlayer is None:
            raise RuntimeError('Current player has not been set yet')
        return self.currentPlayer

    def _clearScreen(self) -> None:
        """Clears terminal screen based on operating system"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _moveCursor(self, key: str) -> None:
        """Moves cursor based on keyboard input and navigation map."""
        if key in navigation[self.cursorPosition]:
            self.cursorPosition = navigation[self.cursorPosition][key]

    def _endTurn(self) -> None:

        """Ends current players turn and passes turn"""

        currentPlayer = self._requirePlayer()

        if currentPlayer.tilesTakenOut == 15:
            self.winner = currentPlayer.color
            return
        if currentPlayer.color == 'white':
            self.currentPlayer = self.players['black']
        else:
            self.currentPlayer = self.players['white']
        self.lastMoves.clear()
        self.usedDice.clear()
        self.remainingMoves = list(throwDice())

    def _undo(self, currentPlayer) -> None:

        """Undos previous moves from a 'movestack'"""

        if not self.lastMoves:
            return

        moveData = self.lastMoves.pop()

        fromPos = moveData['from']
        toPos = moveData['to']
        diceValue = moveData['dice']
        hitData = moveData['hit']
        bearOff = moveData['bearOff']

        if bearOff:
            self.board.addTile(fromPos, Tile(currentPlayer.color))
            currentPlayer.tilesTakenOut -= 1
        else:
            self.board.moveTile(toPos, fromPos)
        self.remainingMoves.insert(0, diceValue)

        if hitData:
            if hitData['bar'] == 25: #White bar
                self.board.moveTile(25, hitData['position'])
            else:
                self.board.moveTile(0, hitData['position'])

        if self.usedDice:
            self.usedDice.pop()
    
    def _simulateMove(self, board: Board, player: Player, move: tuple) -> Board | None:
        newBoard = deepcopy(board)
        endGame = board.checkForEndgame(player)
        fromPos, toPos = move[0], move[1]
        
        """Validates and makes a move on a copy of Board class."""

        if not self._columnBelongsToCurrentPlayer(newBoard, player, fromPos):
            return None

        validEndgame = self._checkValidEndGameMove(newBoard, player, fromPos, toPos)
        validMove = self._isLegalMove(board, player, fromPos, toPos)

        if endGame and validEndgame and validMove:
            newBoard.bearOffTile(fromPos)
        else:
            if 1 <= toPos <= 24 and not self._checkForBlockedColumn(newBoard, 
                                                                    player, toPos):
                hittile = self._getHittableTile(newBoard, player, toPos)
                if hittile:
                    bar = 25 if hittile.color == 'white' else 0
                    newBoard.moveTile(toPos, bar)
            newBoard.moveTile(fromPos, toPos)
        return newBoard

    def getLegalMoveSequences(
            self, board: Board, player: Player, 
            dice: list[int]) -> list[list[tuple]]:
        """Used to make sure the largest amount of dice are used."""
        moveSequences: list[list[tuple]] | list = []

        def depthSearch(
                board: Board, player: Player, 
                remainingDice: list[int], 
                sequence: list[tuple]) -> None:
            """Searches for all possible move sequences recursively"""
            if not remainingDice: #Basecase
                moveSequences.append(sequence)
                return

            legalMovesLeft = False

            for die in set(remainingDice): #Use set here to avoid trying the same die 
                #on the same board. Since doubles reversed doesnt change the dice
                #it is unnecessary to use enumerate()
                legalMoves = self.getAllLegalSingleMoves(board, player, die)

                for move in legalMoves:
                    legalMovesLeft = True

                    newBoard = self._simulateMove(board, player, move)
                    if newBoard == None:
                        continue
                    newRemainingDice = list(remainingDice)
                    newRemainingDice.remove(die)

                    depthSearch(newBoard, player, 
                                newRemainingDice, 
                                sequence + [move])
            
            if not legalMovesLeft:
                moveSequences.append(sequence)

        depthSearch(board, player, dice, [])

        maxLengthSequence: int = max(len(seq) for seq in moveSequences)

        longestSequences: list[list[tuple]] = [seq for seq in moveSequences 
                            if len(seq) == maxLengthSequence]

        return longestSequences

    def getRequiredMoveSequence(self, board: Board, 
                                player: Player, 
                                dice: list[int]) -> list[list[tuple]]:

        """First gets all possible legal move sequences. Then checks against
        a rule that says if all sequences results in only 1 die being
        used. The larger of the dice must be used"""

        moveSequences = self.getLegalMoveSequences(board, player, dice)
        if not moveSequences:
            return moveSequences

        maxLengthOfSequence = len(moveSequences[0])

        if maxLengthOfSequence == 1 and len(dice) > 1:
            highestDice = dice[0] if dice[0] >= dice[1] else dice[1]

            highDieSequences = [
                    seq for seq in moveSequences
                    if seq and seq[0][2] == highestDice]

            if highDieSequences:
                moveSequences = highDieSequences
        return moveSequences

    def _columnBelongsToCurrentPlayer(self, board: Board, 
                                      player: Player, 
                                      position: int) -> bool:
        """Checks if the selected column at position is housing a tile/checker
        of current players color"""

        currentPlayer = player
        tiles = board.getTilesAt(position)
        if not tiles:
            return False
        return tiles[-1].color == currentPlayer.color

    def _getHittableTile(self, board: Board, 
                         player: Player, 
                         position: int) -> Tile | None:
        
        """Checks if a tile/checker is able to be hit at position"""

        currentPlayer = player
        tiles = board.getTilesAt(position)
        if len(tiles) == 1 and tiles[-1].color != currentPlayer.color:
            return tiles[-1]
        else:
            return None

    def _hitTile(self, board: Board, position: int) -> dict | None:

        """
        'Hits' the lone tile placed at position and moves it to its 'bar'.
        """

        tiles = board.getTilesAt(position)
        if not len(tiles) == 1:
            return
        
        hitTile = tiles[-1]
        
        if tiles[-1].color == 'white':
            board.moveTile(position, 25)#Send to white bar.
            bar = 25#Used for undo function.
        else:
            board.moveTile(position, 0)#Send to black bar.
            bar = 0
        return {
                'tile': hitTile,
                'bar': bar,
                'position': position
                }

    def _checkForBlockedColumn(self, board: Board, 
                               player: Player, 
                               position: int) -> bool:
        """Checks if player is trying to move onto
        opponents 'blocked' column. Meaning a column with 2
        or more checkers with the color of the opponent"""

        currentPlayer = player
        tiles = board.getTilesAt(position)
        
        if len(tiles) > 1 and tiles[-1].color != currentPlayer.color:
            return True
        return False

    def _checkValidEndGameMove(self, board: Board, player: Player, 
                               fromPos: int, toPos: int) -> bool:
        
        """Validates move against 'bearoff' logic"""

        if player.color == 'white' and toPos == 0:
            return True

        if player.color == 'black' and toPos == 25:
            return True
        
        if player.color == 'white' and toPos < 0:
            for i in range(fromPos + 1, 6 + 1):
                if self._columnBelongsToCurrentPlayer(board, player, i):
                    return False    
            return True
        if player.color == 'black' and toPos > 25:
            for i in range(fromPos - 1, 19 - 1, -1):
                if self._columnBelongsToCurrentPlayer(board, player, i):
                    return False    
            return True
        return False
        
    def _isLegalMove(self, board: Board, player: Player, 
                     fromPos: int, toPos: int) -> bool:
        
        """A legal check for trying to make a move.
        used in simulating moves and getAllLegalSingleMoves method"""

        barred = board.checkBarredCheckers(player)
        currentPlayerBar = 25 if player.color == 'white' else 0
        if barred and fromPos != currentPlayerBar:
            return False
        
        if not self._columnBelongsToCurrentPlayer(board, player, fromPos):
            return False
        

        endGame = board.checkForEndgame(player)

        if not endGame and not (1 <= toPos <= 24): 
            return False

        if endGame and not (1 <= toPos <= 24): 
            return self._checkValidEndGameMove(board, player, fromPos, toPos)

        if self._checkForBlockedColumn(board, player, toPos):
            return False
        #Need a canBearOff function
        return True

    def getAllLegalSingleMoves(
            self, board: Board, player: Player, 
            die: int) -> list[tuple]:
        """Gets all moves that are possible with a single die
        also used when calculating all possible moves"""

        moves = []

        barred = board.checkBarredCheckers(player)
        if barred:
            fromPositions = [25] if player.color == 'white' else [0]
        else:
            fromPositions = [pos for pos in range(1, 25)]

        for fromPos in fromPositions:
            toPos = fromPos + (die * player.direction)
            if self._isLegalMove(board, player, fromPos, toPos):
                moves.append((fromPos, toPos, die))
        return moves

    def _selectColumn(self) -> None:
        """
        Tries to move piece based on the current position
        of cursor. Validates move to see if it is legal.
        """
        if not self.remainingMoves:
            return

        currentPlayer = self._requirePlayer()
        
        legalMoves = self.getRequiredMoveSequence(self.board, currentPlayer,
                                                  self.remainingMoves)
        
        if not legalMoves:
            self._endTurn()
            return

        endGame = self.board.checkForEndgame(currentPlayer)

        diceValue = self.remainingMoves[0]
        fromPos = self.cursorPosition
        toPos = fromPos + (diceValue * currentPlayer.direction)

        move = (fromPos, toPos, diceValue)

        allowedFirstMoves = [seq[0] for seq in legalMoves if seq]
        
        currentDieLegalMoves = self.getAllLegalSingleMoves(self.board, currentPlayer,
                                                           diceValue)
        
        if move not in currentDieLegalMoves:
            currentPlayer.showIllegalMoveMessage = False
            return

        if move not in allowedFirstMoves:
            currentPlayer.showIllegalMoveMessage = True
            return

        hitData = None
        if 1 <= toPos <= 24 and self._getHittableTile(self.board, currentPlayer, toPos):
            hitData = self._hitTile(self.board, toPos)
        
        bearOff = False
        if endGame and (toPos <= 0 or toPos >= 25):
                self.board.bearOffTile(fromPos)
                bearOff = True
                currentPlayer.tilesTakenOut += 1
        else: 
            self.board.moveTile(fromPos, toPos)

        moveData = {
            'from': fromPos,
            'to': toPos,
            'dice': diceValue,
            'hit': hitData,
            'bearOff': bearOff
            }

        self.usedDice.append(self.remainingMoves.pop(0))
        self.lastMoves.append(moveData)
        currentPlayer.showIllegalMoveMessage = False
        
    def _rollStartingDice(self) -> None:
        """Rolls starting round dice and calculates 
        starting playerbased on the outcome"""
        while True: #Change to something more readable
            whiteDie = throwDice()[0]
            blackDie = throwDice()[0]

            if whiteDie != blackDie:
                self.firstDiceWhite = whiteDie
                self.firstDiceBlack = blackDie

                if whiteDie > blackDie:
                    self.currentPlayer = self.players['white']
                else:
                    self.currentPlayer = self.players['black']

                self.remainingMoves = [whiteDie, blackDie]
                return

    def getCurrentPlayer(self) -> Player | None:
        """A getter for current player"""
        return self.currentPlayer

    def getWinner(self, players: dict[str, Player]) -> str | None:
        """
        Calculates winner based on number 
        of checkers left in each of 4 zones
        and adds appropriate amount of wins to player
        """
        zoneOne = self.board.getColorsInZone(1)
        zoneTwo = self.board.getColorsInZone(2)
        zoneThree = self.board.getColorsInZone(3)
        zoneFour = self.board.getColorsInZone(4)
        sumOfTilesWhite = zoneOne['white'] + zoneTwo['white'] + zoneThree['white'] + zoneFour['white']
        sumOfTilesBlack = zoneFour['black'] + zoneThree['black'] + zoneTwo['black'] + zoneOne['black']
        #This way of calculating winner based on sumOfTiles makes it possible
        #to set up your own homegame with different amount and placing of starting checkers.
        if sumOfTilesWhite == 0 and not self.debug:
            self._winGame(players['white'], players)
            return 'white'
        elif sumOfTilesBlack == 0 and not self.debug:
            self._winGame(players['black'], players)
            return 'black'
        return None

    def _winGame(self, winningPlayer: Player, players) -> None:
        if winningPlayer.gamesWon >= self.firstToWins:
            return
        gameIsWorth: int = self.board.getWinningPoints(winningPlayer, players)
        winningPlayer.gamesWon += gameIsWorth * self.doublingcube.value
        self.gameWon = True


    def start(self) -> None:
        """Starts the renderloop, handles input and checks state"""
        while self.state.isState('main-menu'):
            self._clearScreen()
            self.menuRenderer.renderMenu(self.mainmenu.menu)
            key: str = getKey().lower()
            self.mainmenu.handleInput(key)
            self.firstToWins = self.mainmenu.menu.points

        while self.state.isState('running') and not self.gameWon:
            debug = self.debug == True and self.debugSetupDone == True
            self._clearScreen()
            if self.startingRound:
                self._rollStartingDice()
                self.startingRound = False
                continue

            if self.debug and not self.debugSetupDone:
                debugDice = []
                self.board._setupDebugLogicBoard(self.board)
                self.remainingMoves = debugDice
                self._resetController(self.board)
                self.startingRound = False
                self.currentPlayer = self.players['white']
                self.debugSetupDone = True

            renderBoard(self.board, self.players, self.debug,
                self.debugInputController,
                self.getCurrentPlayer, self.cursorPosition, 
                self.doublingcube, self.remainingMoves,
                self.board.getCurrentPipCount, self.getWinner,
                self.firstToWins)

            player = self._requirePlayer()
            key: str = getKey().lower()
            
            if key in ('w', 'a', 's', 'd'):
                self._moveCursor(key)
                player.showIllegalMoveMessage = False

            if key == 'i':
                player.showKeybindHints = not player.showKeybindHints
                
            if debug:
                self.debugInputController.handleDebugInput(key)
            else:
                if key in ('\r', '\n', ' ') and self.remainingMoves:
                    self._selectColumn()
                elif key == 'r':
                    self.remainingMoves.reverse()
                    player.showIllegalMoveMessage = False
                elif key == 'u':
                    self._undo(player)
                elif key in ('\r', '\n', ' ') and not self.remainingMoves:
                    self._endTurn()
                elif key == 'x':
                    self.debug = True
                elif key in ('\x1b', '\033', '\x03'): #ESC or Ctrl+C.
                    self.state.setState('main-menu')
                    self.start()

            

        



