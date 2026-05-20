from model.board import Board
from model.doublingcube import DoublingCube
from model.player import Player


def _getTileColor(tile):
    return ' ◖◗ ' if tile.color == 'white' else '\x1b[31m ◖◗ \x1b[0m' 

def _getColumn(board, position, fromTop = False, height = 5):
    tiles = board.getTilesAt(position)
    visibleTiles = tiles[:height]
    column = [_getTileColor(tile) for tile in visibleTiles]
    if len(tiles) > height:
        column[4] = f" {len(tiles)} " if len(tiles) > 9 else f" 0{len(tiles)} "  
    while len(column) < height:
        column.append("    ")

    if not fromTop:
        column.reverse()

    return column

def _renderCursorTop(cursorPos):
    positions = [24, 23, 22, 21, 20, 19, 0, 18, 17, 16, 15, 14, 13]
    cursorRow = "     "
    for pos in positions:
        if pos == 0:
            cursorRow += "    ▼    " if pos == cursorPos else "         " 
        else:
            cursorRow += "  ▼  " if pos == cursorPos else "     "
    return cursorRow

def _renderCursorBottom(cursorPos):
    positions = [1, 2, 3, 4, 5, 6, 25, 7, 8, 9, 10, 11, 12]
    cursorRow = "     "
    for pos in positions:
        if pos == 25:
            cursorRow += "    ▲    " if pos == cursorPos else "         "
        else:
            cursorRow += "  ▲  " if pos == cursorPos else "     "
    return cursorRow
def renderBoard(board: Board, players: dict[str, Player],
                debug: bool, debugInputController,
                getCurrentPlayer, cursorPos: int, 
                cube: DoublingCube, dice: list[int], 
                getPipCount, _getGameWinner, firstToWins: int):


    topLeftPositions = [24, 23, 22, 21, 20, 19]
    topRightPositions = [18, 17, 16, 15, 14, 13]
    bottomRightPositions = [7,8, 9, 10, 11, 12]
    bottomLeftPositions = [1, 2, 3, 4, 5, 6]

    topColumns = {}
    bottomColumns = {}
    topBar = _getColumn(board, 0, fromTop=False)
    bottomBar = _getColumn(board, 25, fromTop=True)
    
    currentPlayer: Player = getCurrentPlayer()
    winner: str = _getGameWinner(board)#'white' or 'black'
    pipCountWhite, pipCountBlack = getPipCount()
    

    blackIllegal = (
            currentPlayer.color == 'black'
            and currentPlayer.showIllegalMoveMessage
            )
    whiteIllegal = (
            currentPlayer.color == 'white'
            and currentPlayer.showIllegalMoveMessage
            )
    illegalMessage = 'You must play all dice if possible.'.rjust(47)

    for position in topLeftPositions + topRightPositions:
        topColumns[position] = _getColumn(board, position, fromTop=True)

    for position in bottomLeftPositions + bottomRightPositions:
        bottomColumns[position] = _getColumn(board, position)
    print(f"Wins: {players['black'].gamesWon}")
    print(f"   Pip: {pipCountBlack}", end='')
    print(f"First to {firstToWins} wins.".rjust(37))
    print(f"    OFF: {players['black'].tilesTakenOut}", end='')    
    print(illegalMessage if blackIllegal else '')
    if currentPlayer.color == 'black':
        if not dice:
            print("Press enter to pass turn".rjust(51))
        else:
            print(f"{dice}".rjust(41))
    else:
        print()
    if winner == 'black' and not debug:
        print("Winner: black".rjust(45))
    elif players['black'].hasDoubled:
        print(f"Cube: {cube.value}")
    print(_renderCursorTop(cursorPos))
    print("    ┌────┬────┬────┬────┬────┬────┬────────┬────┬────┬────┬────┬────┬────┐")
    print("    │ 24 │ 23 │ 22 │ 21 │ 20 │ 19 │        │ 18 │ 17 │ 16 │ 15 │ 14 │ 13 │")
    print("    ├────┼────┼────┼────┼────┼────┼────────┼────┼────┼────┼────┼────┼────┤")

    for row in range(5):
        leftSide = "".join(f"│{topColumns[pos][row]}" for pos in topLeftPositions)
        rightSide = "".join(f"│{topColumns[pos][row]}" for pos in topRightPositions)
        print(f"    {leftSide}│  {topBar[row]}  {rightSide}│")

    print("    ├────┼────┼────┼────┼────┼────┼────────┼────┼────┼────┼────┼────┼────┤")

    for row in range(5):
        leftSide = "".join(f"│{bottomColumns[pos][row]}" for pos in bottomLeftPositions)
        rightSide = "".join(f"│{bottomColumns[pos][row]}" for pos in bottomRightPositions)
        print(f"    {leftSide}│  {bottomBar[row]}  {rightSide}│")

    print("    ├────┼────┼────┼────┼────┼────┼────────┼────┼────┼────┼────┼────┼────┤")
    print("    │  1 │  2 │  3 │  4 │  5 │  6 │        │  7 │  8 │  9 │ 10 │ 11 │ 12 │")
    print("    └────┴────┴────┴────┴────┴────┴────────┴────┴────┴────┴────┴────┴────┘")
    print(_renderCursorBottom(cursorPos))
    if winner == 'white' and not debug:
        print("Winner: white".rjust(45))
    elif players['white'].hasDoubled:
        print(f"Cube: {cube.value}")
    if currentPlayer.color == 'white':
        if not dice:
            print("Press enter to pass turn".rjust(51))
        else:
            print(f"{dice}".rjust(41))
    else:
        print()
    print(f"    OFF: {players['white'].tilesTakenOut}", end='')    
    print(illegalMessage if whiteIllegal else '')
    print(f"   Pip: {pipCountWhite}", end='')
    
    print("[i] = Show/hide controls".rjust(40))

    print(f"Wins: {players['white'].gamesWon}")
    
    if not debug and currentPlayer.showKeybindHints:
        print("[W] [A] [S] [D] or Arrows = Move cursor".rjust(45), end=' | ')
        print("[U] = Undo")
        print("[R] = Reverse order of dice".rjust(45), end=' | ')
        print("[X] = Sandbox mode")
        print("[Enter] or [Space] = Select piece to move".rjust(45), end=' | ')
        print("Hold [ESC] = Quit")
        print("[Q] = Main Menu".rjust(46))
    elif debug:
        print("==============[Sandbox mode]==============".rjust(60))
        if currentPlayer.showKeybindHints:
            print("[1 - 2] = Switch to placing white or black pieces".rjust(62), end='')
            print(f"  [{debugInputController.currentlyPlacingTile}]")
            print("[3 - 4] = Change value of dice".rjust(43))
            print("[Backspace] = Remove checker/tile".rjust(46))
            print("[Enter] or [Space] = Place piece".rjust(45), end=' | ')
            print("[C] = Clear board")
            print("[F] = Change current player".rjust(40))
            print("[X] = Exit from sandbox mode".rjust(41))
            print("Hold [ESC] = Quit".rjust(25))


