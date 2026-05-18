class MainMenu:
    def __init__(self, state) -> None:
        self.state = state

        self.header = True

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
                '║                THE CLASSIC GAME OF STRATEGY                ║',
                '║                                                            ║',
                '╚════════════════════════════════════════════════════════════╝'
                ]
        return header

    def _updateOptions(self):
        self.options = ['START', f'FIRST TO: {self.points}']

    def moveUp(self):
        self.hovering = (self.hovering + 1) % len(self.options)

    def moveDown(self):
        self.hovering = (self.hovering - 1) % len(self.options)

    def selectOptions(self):
        if self.hovering == 0:
            self.state.setState('running')
        elif self.hovering == 1:
            self.points = (self.points + 2) % 10
        self._updateOptions()
