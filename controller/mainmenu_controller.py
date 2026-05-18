class MenuController:
    def __init__(self, menu, state):
        
        self.state = state
        self.menu = menu(self.state)

    def handleInput(self, key: str):
        if key == 'w':
            self.menu.moveUp()
        elif key == 's':
            self.menu.moveDown()
        elif key in ('\r', '\n'):
            self.menu.selectOptions()
        elif key in ('\x1b', '\033', '\x03'):
            if self.state.isState('main-menu'):
                self.state.setState('exit')
            else:
                self.state.setState('main-menu')
