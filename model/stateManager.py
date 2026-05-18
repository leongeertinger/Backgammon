class StateManager:
    def __init__(self):
        self.state = 'main-menu'

    def isState(self, state: str):
        if state == self.state:
            return True
        return False
    def setState(self, state: str) -> None:
        state = state.lower().strip()

        if state not in ('running', 'main-menu', 'exit'):
            return None
        else:
            self.state = state
