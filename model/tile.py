class Tile:
    idCounter = 0 #Have not implemented a use for this yet.
    def __init__(self, color: str) -> None:
        self.id = Tile.idCounter
        Tile.idCounter += 1
        self.color = color

