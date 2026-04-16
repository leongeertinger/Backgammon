import sys

def getKey():
    if sys.platform.startswith('win'):
        import msvcrt
        return msvcrt.getwch()

    else:
        import tty
        import termios

        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
