import sys
from PyQt5.QtWidgets import QApplication
from controllers.main_controller import MainController
from models.schedule_model import ScheduleModel
from views.builders.view_builder import MainViewBuilder
from views.builders.theme_factory import LightThemeFactory

def main():
    """Application entry point"""
    app = QApplication(sys.argv)
    
    # Initialize model
    model = ScheduleModel()
    
    # Set up view with builder and abstract factory patterns
    theme_factory = LightThemeFactory()
    view_builder = MainViewBuilder(theme_factory)
    
    # Initialize controller
    controller = MainController(model, view_builder)
    
    # Show main window and start app
    controller.show_main_view()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
