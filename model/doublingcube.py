from model.player import Player


class DoublingCube:
    def __init__(self):
        self.value = 1
        self.playerLastDoubled: Player | None = None

    def double(self, player: Player) -> None:
        if player == self.playerLastDoubled:
            return
        if self.value == 1:
            self.value = 2
        else: 
            self.value **= 2
        self.playerLastDoubled = player
