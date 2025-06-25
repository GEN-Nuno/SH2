class ViewBuilder:
    def __init__(self):
        self.views = {}

    def add_view(self, name, view):
        self.views[name] = view

    def get_view(self, name):
        return self.views.get(name)

    def build(self):
        # Logic to construct views can be added here
        pass