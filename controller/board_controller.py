from model.board import Board
from views.board_view import renderBoard
from model.dice import throwDice
from controller.input_handler import getKey
from model.doublingcube import DoublingCube
from model.player import Player
from model.navigation import navigation
from copy import deepcopy
import os


class BoardController:
    def __init__(self):
        self.board = Board()
        self.cursorPosition = 1
        self.remainingMoves = []
        self.usedDice = []
        self.lastMoves = []

        self.players: dict[str, Player] = {
                'white': Player('white', -1),
                'black': Player('black', 1)
                }
        self.firstDiceWhite = None
        self.firstDiceBlack = None
        
        self.currentPlayer: Player | None = None
        self.doublingcube = DoublingCube()

        self.debug = False
        self.debugSetupDone = False
        self.startingRound = True
        self.running = True

    def _requirePlayer(self): #Make sure currenplayer is not None during runtime
        #after it has been set the first time.
        if self.currentPlayer is None:
            raise RuntimeError('Current player has not been set yet')
        return self.currentPlayer

    def _clearScreen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _moveCursor(self, key):
        if key in navigation[self.cursorPosition]:
            self.cursorPosition = navigation[self.cursorPosition][key]

    def _endTurn(self):
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
    
    def _simulateMove(self, board, player, move):
        newBoard = deepcopy(board)

        fromPos, toPos, die = move
        
        if not self._columnBelongsToCurrentPlayer(newBoard, player, fromPos):
            return None

        if board.checkGameState(player) and self._checkValidEndGameMove(newBoard, player, 
                                                                        fromPos, toPos):
            newBoard.bearOffTile(fromPos)
        else:
            if 1 <= toPos <= 24 and not self._checkForBlockedColumn(newBoard, player, toPos):
                hittile = self._getHittableTile(newBoard, player, toPos)
                if hittile:
                    bar = 25 if hittile.color == 'white' else 0
                    newBoard.moveTile(toPos, bar)
            newBoard.moveTile(fromPos, toPos)
        return newBoard

    def getLegalMoveSequences(self, board, player, dice):
        #Used to make sure all dice are used if possible
        moveSequences = []

        def depthSearch(board, player, remainingDice, sequence):
            if not remainingDice: #Basecase
                moveSequences.append(sequence)
                return

            foundMove = False

            for i, die in enumerate(remainingDice):
                legalMoves = self.getAllLegalSingleMoves(board, player, die)

                for move in legalMoves:
                    foundMove = True

                    newBoard = self._simulateMove(board, player, move)
                    if newBoard == None:
                        continue
                    newRemainingDice = remainingDice[:i] + remainingDice[i + 1:]

                    depthSearch(newBoard, player, newRemainingDice, sequence + [move])
            
            if not foundMove:
                moveSequences.append(sequence)

        depthSearch(board, player, dice, [])

        maxLengthSequence = max(len(seq) for seq in moveSequences)

        longestSequences = [seq for seq in moveSequences if len(seq) == maxLengthSequence]

        return longestSequences

    def getRequiredMoveSequence(self, board, player, dice):
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

    def _columnBelongsToCurrentPlayer(self, board, player, position):
        currentPlayer = player
        tiles = board.getTilesAt(position)
        if not tiles:
            return False
        return tiles[-1].color == currentPlayer.color

    def _getHittableTile(self, board, player, position):
        currentPlayer = player
        tiles = board.getTilesAt(position)
        if len(tiles) == 1 and tiles[-1].color != currentPlayer.color:
            return tiles[-1]
        else:
            return None

    def _hitTile(self, board, position):
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

    def _checkForBlockedColumn(self, board, player, position):
        currentPlayer = player
        tiles = board.getTilesAt(position)
        
        if len(tiles) > 1 and tiles[-1].color != currentPlayer.color:
            return True
        return False

    def _checkValidEndGameMove(self, board, player, fromPos, toPos):
        
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
        
    def _isLegalMove(self, board, player, fromPos, toPos):
        barred = board.checkBarredCheckers(player)
        currentPlayerBar = 25 if player.color == 'white' else 0
        if barred and fromPos != currentPlayerBar:
            return False
        
        if not self._columnBelongsToCurrentPlayer(board, player, fromPos):
            return False
        

        endGame = board.checkGameState(player)

        if not endGame and not (1 <= toPos <= 24): 
            return False

        if endGame and not (1 <= toPos <= 24): 
            return self._checkValidEndGameMove(board, player, fromPos, toPos)

        if self._checkForBlockedColumn(board, player, toPos):
            return False
        #Need a canBearOff function
        return True

    def getAllLegalSingleMoves(self, board, player, die):
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

    def _selectColumn(self):
        if not self.remainingMoves:
            return

        currentPlayer = self._requirePlayer()
        
        legalMoves = self.getRequiredMoveSequence(self.board, currentPlayer,
                                                  self.remainingMoves)
        
        if not legalMoves:
            self._endTurn()
            return

        endGame = self.board.checkGameState(currentPlayer)

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
        
        if endGame and (toPos <= 0 or toPos >= 25):
                self.board.bearOffTile(fromPos)
                currentPlayer.tilesTakenOut += 1
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
        currentPlayer.showIllegalMoveMessage = False
        
    def _rollStartingDice(self):
        while True:
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

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getWinner(self):
        white = self.players['white']
        black = self.players['black']
        if white.tilesTakenOut == 15:
            return 'white'
        elif black.tilesTakenOut == 15:
            return 'black'
        return None

    def start(self):
        while self.running:
            self._clearScreen()
            if self.startingRound:
                self._rollStartingDice()
                self.startingRound = False
                continue

            if self.debug and not self.debugSetupDone:
                self.board._setupDebugLogicBoard(self.board)
                self.remainingMoves = [6, 2]
                self.usedDice = []
                self.lastMoves = []
                self.firstDiceWhite = None
                self.firstDiceBlack = None
                self.startingRound = False
                self.currentPlayer = self.players['white']
                self.debugSetupDone = True

            renderBoard(self.board, self.players, self.getCurrentPlayer, self.cursorPosition, 
                        self.doublingcube, self.remainingMoves, 
                        self.firstDiceWhite, self.firstDiceBlack, 
                        self.board.getCurrentPipCount, self.getWinner)
            player = self._requirePlayer()
            key = getKey().lower()
            if key in ('w', 'a', 's', 'd'):
                self._moveCursor(key)
                player.showIllegalMoveMessage = False
            elif key in ('\r', '\n') and self.remainingMoves:
                self._selectColumn()
            elif key == 'r':
                self.remainingMoves.reverse()
                player.showIllegalMoveMessage = False
            elif key == 'u':
                self._undo()
            elif key in ('\r', '\n') and not self.remainingMoves:
                self._endTurn()
            elif key in ('\x1B', '\033'):
                self.running = False
        



