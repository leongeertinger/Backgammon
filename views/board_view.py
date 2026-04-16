def _getTileColor(tile):
    return ' ●● ' if tile.color == 'white' else ' ○○ ' 

def _getColumn(board, position, fromTop = False, height = 5):
    tiles = board.getTilesAt(position)
    visibleTiles = tiles[:height]
    column = [_getTileColor(tile) for tile in visibleTiles]
    if len(tiles) > 5:
        column[4] = f" {len(tiles)} " if len(tiles) > 9 else f" 0{len(tiles)} "  
    while len(column) < height:
        column.append("    ")

    if not fromTop:
        column.reverse()

    return column

def _renderCursorTop(cursorPos):
    positions = [24, 23, 22, 21, 20, 19, None, 18, 17, 16, 15, 14, 13]
    cursorRow = "     "
    for pos in positions:
        if pos == None:
            cursorRow += "         " 
        elif pos == cursorPos:
            cursorRow += "  ▼  "
        else:
            cursorRow += "     "
    return cursorRow

def _renderCursorBottom(cursorPos):
    positions = [1, 2, 3, 4, 5, 6, None, 7, 8, 9, 10, 11, 12]
    cursorRow = "     "
    for pos in positions:
        if pos == None:
            cursorRow += "         " 
        elif pos == cursorPos:
            cursorRow += "  ▲  "
        else:
            cursorRow += "     "
    return cursorRow
def renderBoard(board, cursorPos, dice, firstDiceWhite, firstDiceBlack):
    topLeftPositions = [24, 23, 22, 21, 20, 19]
    topRightPositions = [18, 17, 16, 15, 14, 13]
    bottomRightPositions = [7,8, 9, 10, 11, 12]
    bottomLeftPositions = [1, 2, 3, 4, 5, 6]

    topColumns = {}
    bottomColumns = {}

    for position in topLeftPositions + topRightPositions:
        topColumns[position] = _getColumn(board, position, fromTop=True)

    for position in bottomLeftPositions + bottomRightPositions:
        bottomColumns[position] = _getColumn(board, position)

    print("    OFF:")
    print(_renderCursorTop(cursorPos))
    print("    ┌────┬────┬────┬────┬────┬────┬────────┬────┬────┬────┬────┬────┬────┐")
    print("    │ 24 │ 23 │ 22 │ 21 │ 20 │ 19 │        │ 18 │ 17 │ 16 │ 15 │ 14 │ 13 │")
    print("    ├────┼────┼────┼────┼────┼────┼────────┼────┼────┼────┼────┼────┼────┤")

    for row in range(5):
        leftSide = "".join(f"│{topColumns[pos][row]}" for pos in topLeftPositions)
        rightSide = "".join(f"│{topColumns[pos][row]}" for pos in topRightPositions)
        print(f"    {leftSide}│        {rightSide}│")

    print("    ├────┼────┼────┼────┼────┼────┼────────┼────┼────┼────┼────┼────┼────┤")

    for row in range(5):
        leftSide = "".join(f"│{bottomColumns[pos][row]}" for pos in bottomLeftPositions)
        rightSide = "".join(f"│{bottomColumns[pos][row]}" for pos in bottomRightPositions)
        print(f"    {leftSide}│        {rightSide}│")

    print("    ├────┼────┼────┼────┼────┼────┼────────┼────┼────┼────┼────┼────┼────┤")
    print("    │  1 │  2 │  3 │  4 │  5 │  6 │        │  7 │  8 │  9 │ 10 │ 11 │ 12 │")
    print("    └────┴────┴────┴────┴────┴────┴────────┴────┴────┴────┴────┴────┴────┘")
    print(_renderCursorBottom(cursorPos))
    print("    OFF:")
    print("W, A, S, D = Move cursor".rjust(51))
    print("U = Undo".rjust(44))
    print("R = Reverse order of dice".rjust(44))
    print("E = Double".rjust(44))
    print("Enter = Select piece to move".rjust(60))
    print("ESC = Quit".rjust(44))


