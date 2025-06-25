from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QTextEdit, QPushButton, QComboBox,
                            QCheckBox, QGridLayout, QGroupBox)
from PyQt5.QtCore import Qt

class TaskDetailView(QDialog):
    """Dialog for displaying and editing task details"""
    
    def __init__(self, theme_factory, task, controller=None):
        super().__init__()
        self.theme_factory = theme_factory
        self.colors = theme_factory.create_color_scheme()
        self.fonts = theme_factory.create_font_scheme()
        self.setStyleSheet(theme_factory.create_style_sheet())
        
        self.task = task
        self.controller = controller
        
        self.setWindowTitle(f"Task Detail: {task.name}")
        self.setMinimumSize(500, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        layout = QVBoxLayout(self)
        
        # Task details form
        form_layout = QGridLayout()
        
        # Task name
        form_layout.addWidget(QLabel("Task Name:"), 0, 0)
        self.name_edit = QLineEdit(self.task.name)
        form_layout.addWidget(self.name_edit, 0, 1)
        
        # Task status
        form_layout.addWidget(QLabel("Status:"), 1, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems(["working", "planned", "closed"])
        self.status_combo.setCurrentText(self.task.status)
        form_layout.addWidget(self.status_combo, 1, 1)
        
        # Days
        days_group = QGroupBox("Days")
        days_layout = QHBoxLayout(days_group)
        self.day_checkboxes = {}
        
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Free"]:
            checkbox = QCheckBox(day)
            checkbox.setChecked(day in self.task.days)
            days_layout.addWidget(checkbox)
            self.day_checkboxes[day] = checkbox
        
        form_layout.addWidget(days_group, 2, 0, 1, 2)
        
        # Completion checkbox
        form_layout.addWidget(QLabel("Completed Today:"), 3, 0)
        self.completed_check = QCheckBox()
        self.completed_check.setChecked(self.task.completed_today)
        form_layout.addWidget(self.completed_check, 3, 1)
        
        # Perceived effort
        form_layout.addWidget(QLabel("Perceived Effort:"), 4, 0)
        self.effort_edit = QLineEdit(str(self.task.perceived_effort))
        form_layout.addWidget(self.effort_edit, 4, 1)
        
        # Task details
        form_layout.addWidget(QLabel("Details:"), 5, 0, Qt.AlignTop)
        self.details_edit = QTextEdit(self.task.details)
        form_layout.addWidget(self.details_edit, 5, 1)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_task)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
    
    def save_task(self):
        """Save task changes"""
        if not self.controller:
            self.reject()
            return
        
        # Get selected days
        selected_days = [day for day, checkbox in self.day_checkboxes.items() if checkbox.isChecked()]
        if not selected_days:
            selected_days = ["Free"]  # Default to Free if no days selected
        
        # Update task attributes
        attributes = {
            "name": self.name_edit.text(),
            "status": self.status_combo.currentText(),
            "days": selected_days,
            "completed_today": self.completed_check.isChecked(),
            "perceived_effort": int(self.effort_edit.text() or 0),
            "details": self.details_edit.toPlainText()
        }
        
        self.controller.update_task(self.task, attributes)
        self.accept()
