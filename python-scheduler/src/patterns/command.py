class Command:
    def __init__(self, action):
        self.action = action

    def execute(self):
        if callable(self.action):
            self.action()
        else:
            raise ValueError("Action must be callable")