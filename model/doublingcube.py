class DoublingCube:
    def __init__(self):
        self.value = 1
        self.playerLastDoubled = None

    def double(self, player):
        if self.value == 1:
            self.value = 2
        else: 
            self.value **= 2
        self.playerLastDoubled = player
