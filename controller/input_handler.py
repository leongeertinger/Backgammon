import sys

def getKey() -> str:
    if sys.platform.startswith('win'): #For windows users
        import msvcrt
        return msvcrt.getwch()

    else: #For mac and or linux users
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
