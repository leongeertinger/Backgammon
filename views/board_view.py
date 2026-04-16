def _getTileColor(tile):
    return ' ●● ' if tile.color == 'white' else ' ○○ ' 

def _getColumn(board, position, fromTop = False, height = 5):
    tiles = board.getTilesAt(position)
    visibleTiles = tiles[:height]
    column = [_getTileColor(tile) for tile in visibleTiles]

    while len(column) < height:
        column.append("    ")

    if not fromTop:
        column.reverse()

    return column

def _renderCursorTop():
    pass

def _renderCursorBottom():
    pass

def renderBoard(board, cursorPos, dice):
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
    print("    OFF:")


