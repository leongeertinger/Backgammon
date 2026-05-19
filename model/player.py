class Player:
    def __init__(self, color: str, direction: int) -> None:
        self.gamesWon = 0
        self.hasDoubled = False
        self.canDouble = True
        self.color = color
        self.direction = direction #-1 or +1
        self.pipCount = 0
        self.tilesTakenOut = 0
        self.showIllegalMoveMessage = False
        self.showKeybindHints = False
        

