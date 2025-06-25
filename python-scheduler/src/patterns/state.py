class State:
    def __init__(self, context):
        self.context = context

    def handle(self):
        pass


class ConcreteStateA(State):
    def handle(self):
        print("Handling state A")
        self.context.set_state(ConcreteStateB(self.context))


class ConcreteStateB(State):
    def handle(self):
        print("Handling state B")
        self.context.set_state(ConcreteStateA(self.context))


class Context:
    def __init__(self, state: State):
        self._state = state

    def set_state(self, state: State):
        self._state = state

    def request(self):
        self._state.handle()