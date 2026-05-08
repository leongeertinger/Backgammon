import sys

def getKey() -> str:
    if sys.platform.startswith('win'): #For windows users
        import msvcrt

        key = msvcrt.getwch()

        if key in ('\x00', '\xe0'):
            second = msvcrt.getwch()
            return {
                'H': 'w',
                'P': 's',
                'M': 'd',
                'K': 'a',
            }.get(second, key)

        return key

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
            
            key = sys.stdin.read(1)
            
            if key == "\x1b":
                nextChars = sys.stdin.read(2)

                arrowMap = {
                    "[A": "w",
                    "[B": "s",
                    "[C": "d",
                    "[D": "a"
                    }
                if nextChars in arrowMap:
                    return arrowMap[nextChars]

            return key
        finally:
            #Återställer settings. I värsta fall så får man
            #starta om sin terminal om den inte återgår till vanligt.
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)


