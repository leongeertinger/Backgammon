class MainMenu:
    def __init__(self, state, _resetController) -> None:
        self.state = state
        
        self._resetController = _resetController

        self.hasHeader = True

        self.showResetMatchIndication = False #Use better solution than this.

        self.options = []

        self.points = 1
        self.hovering = 0

        self._updateOptions()

    def getHeader(self):
        header = [
                '╔════════════════════════════════════════════════════════════╗',
                '║                                                            ║',
                '║                  ██████╗          █████╗                   ║',
                '║                  ██╔══██╗        ██╔════╝                  ║',
                '║                  ██████╔╝        ██║  ███╗                 ║',
                '║                  ██╔══██╗        ██║   ██║                 ║',
                '║                  ██████╔╝ ack    ╚██████╔╝ ammon           ║',
                '║                  ╚═════╝          ╚═════╝                  ║',
                '║                                                            ║',
                '║                        Made by LeonG                       ║',
                '║                                                            ║',
                '╚════════════════════════════════════════════════════════════╝',
                '     [W][S] or [Up][Down] | [Enter] or [Space] to Select',
                '                      Hold [ESC] to quit',
                ''
                ]
        return header

    def _updateOptions(self):
        self.options = ['START', f'FIRST TO: {self.points}', 'RESET MATCH']

    def moveUp(self):
        self.hovering = (self.hovering - 1) % len(self.options)

    def moveDown(self):
        self.hovering = (self.hovering + 1) % len(self.options)

    def selectOptions(self):
        if self.hovering == 0:
            self.showResetMatchIndication = False
            self.state.setState('running')
        elif self.hovering == 1:
            self.points = (self.points + 2) % 10
        elif self.hovering == 2:
            self._resetController(resetMatch = True)
            self.showResetMatchIndication = True

        self._updateOptions()
