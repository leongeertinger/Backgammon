from types import MethodType
from model.board import Board
from model.doublingcube import DoublingCube
from model.player import Player


def _getTileColor(tile):
    return ' ●● ' if tile.color == 'white' else ' ○○ ' 

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
                getCurrentPlayer: MethodType, cursorPos: int, 
                cube: DoublingCube, dice: list[int], firstDiceWhite: int | None, 
                firstDiceBlack: int | None, getPipCount: MethodType, 
                getWinner: MethodType):
    topLeftPositions = [24, 23, 22, 21, 20, 19]
    topRightPositions = [18, 17, 16, 15, 14, 13]
    bottomRightPositions = [7,8, 9, 10, 11, 12]
    bottomLeftPositions = [1, 2, 3, 4, 5, 6]

    topColumns = {}
    bottomColumns = {}
    topBar = _getColumn(board, 0, fromTop=True)
    bottomBar = _getColumn(board, 25)
    
    currentPlayer = getCurrentPlayer()
    winner = getWinner()#'white' or 'black'
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

    print(f"   Pip: {pipCountBlack}")
    print(f"    OFF: {players['black'].tilesTakenOut}", end='')    
    print(illegalMessage if blackIllegal else '')
    print(f"                                   {dice if currentPlayer.color == 'black' else ''}")
    if winner == 'black':
        print("Winner: black".rjust(45))
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
    if winner == 'white':
        print("Winner: white".rjust(45))
    print(f"                                   {dice if currentPlayer.color =='white' else ''}")
    print(f"    OFF: {players['white'].tilesTakenOut}", end='')    
    print(illegalMessage if whiteIllegal else '')
    print(f"   Pip: {pipCountWhite}")
    print("[W] [A] [S] [D] = Move cursor".rjust(45), end=' | ')
    print("[U] = Undo")
    print("[R] = Reverse order of dice".rjust(45), end=' | ')
    print("[E] = Double")
    print("[Enter] = Select piece to move".rjust(45), end=' | ')
    print("[ESC] = Quit")


