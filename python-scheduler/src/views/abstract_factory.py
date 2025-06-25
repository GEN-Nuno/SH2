class AbstractFactory:
    def create_button(self):
        raise NotImplementedError("You should implement this method.")

    def create_label(self):
        raise NotImplementedError("You should implement this method.")

    def create_textbox(self):
        raise NotImplementedError("You should implement this method.")