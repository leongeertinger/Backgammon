class Tile:
    idCounter = 0
    def __init__(self, color):
        self.id = Tile.idCounter
        Tile.idCounter += 1
        self.color = color

