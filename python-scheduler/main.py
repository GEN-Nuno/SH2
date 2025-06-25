import sys
from PyQt5.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    controller = MainController(main_window)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()