class DoublingCube:
    def __init__(self):
        self.value = 0
        self.playerLastDoubled = None

    def double(self, player):
        if self.value == 0:
            self.value = 2
        else: 
            self.value **= 2
        self.playerLastDoubled = player
