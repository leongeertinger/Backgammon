import sys

def getKey():
    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.getwch()

    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        #Sparar terminalens settings innan vi sätter rawmode
        oldSettings = termios.tcgetattr(fd)

        try:
            #Sätter rawmode för att slippa trycka enter efter varje input.
            #Stänge av terminal echo så man inte ser sin egna input.
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            #Återställer settings. I värsta fall så får man
            #starta om sin terminal om den inte återgår till vanligt.
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
