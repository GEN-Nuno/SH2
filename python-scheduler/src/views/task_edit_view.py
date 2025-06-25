from PyQt5 import QtWidgets, QtCore

class TaskEditView(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TaskEditView, self).__init__(parent)
        self.setWindowTitle("タスク編集")
        self.setGeometry(100, 100, 400, 300)
        
        self.layout = QtWidgets.QVBoxLayout(self)

        self.task_name_label = QtWidgets.QLabel("タスク名:")
        self.layout.addWidget(self.task_name_label)

        self.task_name_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.task_name_input)

        self.status_label = QtWidgets.QLabel("状態:")
        self.layout.addWidget(self.status_label)

        self.status_combo = QtWidgets.QComboBox(self)
        self.status_combo.addItems(["working", "planned", "closed"])
        self.layout.addWidget(self.status_combo)

        self.estimated_time_label = QtWidgets.QLabel("体感時間:")
        self.layout.addWidget(self.estimated_time_label)

        self.estimated_time_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.estimated_time_input)

        self.save_button = QtWidgets.QPushButton("保存", self)
        self.save_button.clicked.connect(self.save_task)
        self.layout.addWidget(self.save_button)

        self.delete_button = QtWidgets.QPushButton("削除", self)
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

    def save_task(self):
        # Logic to save the task
        task_name = self.task_name_input.text()
        status = self.status_combo.currentText()
        estimated_time = self.estimated_time_input.text()
        # Save logic goes here

    def delete_task(self):
        # Logic to delete the task
        # Delete logic goes here
        pass