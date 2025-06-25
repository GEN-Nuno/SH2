from PyQt5 import QtWidgets, QtCore

class ScheduleEditView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(ScheduleEditView, self).__init__(parent)
        self.setWindowTitle("Schedule Edit")
        self.setGeometry(100, 100, 600, 400)
        
        self.layout = QtWidgets.QVBoxLayout(self)

        self.task_name_label = QtWidgets.QLabel("Task Name:")
        self.layout.addWidget(self.task_name_label)

        self.task_name_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.task_name_input)

        self.status_label = QtWidgets.QLabel("Status:")
        self.layout.addWidget(self.status_label)

        self.status_combo = QtWidgets.QComboBox(self)
        self.status_combo.addItems(["Working", "Planned", "Closed"])
        self.layout.addWidget(self.status_combo)

        self.day_label = QtWidgets.QLabel("Days:")
        self.layout.addWidget(self.day_label)

        self.day_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.day_input)

        self.details_label = QtWidgets.QLabel("Task Details:")
        self.layout.addWidget(self.details_label)

        self.details_input = QtWidgets.QTextEdit(self)
        self.layout.addWidget(self.details_input)

        self.tag_label = QtWidgets.QLabel("Tag:")
        self.layout.addWidget(self.tag_label)

        self.tag_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.tag_input)

        self.add_button = QtWidgets.QPushButton("Add Task", self)
        self.layout.addWidget(self.add_button)

        self.delete_button = QtWidgets.QPushButton("Delete Task", self)
        self.layout.addWidget(self.delete_button)

        self.save_button = QtWidgets.QPushButton("Save Changes", self)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)