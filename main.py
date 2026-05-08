#!/usr/bin/python3

from controller.board_controller import BoardController

def main():
    game = BoardController()
    game.start()

if __name__ == '__main__':
    main()
