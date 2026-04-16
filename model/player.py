class Player:
    def __init__(self, color, direction) -> None:
        self.canDouble = True
        self.color = color
        self.direction = direction #-1 or +1
        self.pipCount = 0
        self.canTakeTurn = True
        self.tilesTakenOut = 0
        self.tilesHit = 0
        

