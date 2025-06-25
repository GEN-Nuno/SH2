class Strategy:
    def __init__(self):
        self.strategy = None

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_strategy(self, *args, **kwargs):
        if self.strategy is not None:
            return self.strategy.execute(*args, **kwargs)
        else:
            raise ValueError("Strategy not set")

class ConcreteStrategyA:
    def execute(self, data):
        # Implementation for strategy A
        return f"Strategy A executed with data: {data}"

class ConcreteStrategyB:
    def execute(self, data):
        # Implementation for strategy B
        return f"Strategy B executed with data: {data}"