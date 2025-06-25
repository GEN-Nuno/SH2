class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            return []

    def save_config(self, data):
        with open(self.config_file, 'w') as file:
            file.writelines(data)

    def get_config(self):
        return self.config_data

    def update_config(self, new_data):
        self.config_data = new_data
        self.save_config(new_data)