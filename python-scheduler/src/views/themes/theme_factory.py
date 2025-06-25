class ThemeFactory:
    def create_theme(self, theme_type):
        if theme_type == "light":
            return LightTheme()
        elif theme_type == "dark":
            return DarkTheme()
        else:
            raise ValueError("Unknown theme type")

class LightTheme:
    def apply(self):
        # Apply light theme settings
        pass

class DarkTheme:
    def apply(self):
        # Apply dark theme settings
        pass