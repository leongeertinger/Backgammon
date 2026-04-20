from random import randint

def throwDice():
    diceOne = randint(1, 6)
    diceTwo = randint(1, 6)
    if diceOne == diceTwo:
        return diceOne, diceTwo, diceOne, diceTwo
    return diceOne, diceTwo

