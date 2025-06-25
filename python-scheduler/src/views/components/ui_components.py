from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit, QCheckBox, QVBoxLayout, QWidget

class TaskButton(QPushButton):
    def __init__(self, label, *args, **kwargs):
        super().__init__(label, *args, **kwargs)

class TaskLabel(QLabel):
    def __init__(self, text, *args, **kwargs):
        super().__init__(text, *args, **kwargs)

class TaskInput(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class StatusComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addItems(["working", "planned", "closed"])

class TimeEstimateInput(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TaskCheckBox(QCheckBox):
    def __init__(self, label, *args, **kwargs):
        super().__init__(label, *args, **kwargs)

class VerticalLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TaskComponent(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = VerticalLayout()
        self.setLayout(self.layout)

        self.task_label = TaskLabel("Task Name:")
        self.layout.addWidget(self.task_label)

        self.task_input = TaskInput()
        self.layout.addWidget(self.task_input)

        self.status_label = TaskLabel("Status:")
        self.layout.addWidget(self.status_label)

        self.status_combo = StatusComboBox()
        self.layout.addWidget(self.status_combo)

        self.time_estimate_label = TaskLabel("Estimated Time:")
        self.layout.addWidget(self.time_estimate_label)

        self.time_estimate_input = TimeEstimateInput()
        self.layout.addWidget(self.time_estimate_input)

        self.completed_checkbox = TaskCheckBox("Completed")
        self.layout.addWidget(self.completed_checkbox)

        self.save_button = TaskButton("Save")
        self.layout.addWidget(self.save_button)