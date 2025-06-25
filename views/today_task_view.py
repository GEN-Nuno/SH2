from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                            QCheckBox, QMessageBox, QGroupBox, QLineEdit,
                            QComboBox, QTextEdit)
from PyQt5.QtCore import Qt
from datetime import datetime
from models.task_model import Task

class TodayTaskView(QDialog):
    """View for editing today's tasks"""
    
    def __init__(self, theme_factory):
        super().__init__()
        self.theme_factory = theme_factory
        self.colors = theme_factory.create_color_scheme()
        self.fonts = theme_factory.create_font_scheme()
        self.setStyleSheet(theme_factory.create_style_sheet())
        
        self.controller = None
        self.tasks = []
        self.all_tags = []
        self.show_exceptions = False
        self.add_form_visible = False
        
        self.setWindowTitle("本日のタスク編集")
        self.setMinimumSize(800, 600)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
    
    def set_controller(self, controller):
        """Set the controller for this view"""
        self.controller = controller
    
    def set_tasks(self, tasks):
        """Set the tasks to display"""
        self.tasks = tasks
        self.update_task_table()
    
    def set_tags(self, tags):
        """Set available tags"""
        self.all_tags = tags
    
    def build_header(self):
        """Build the header section with title"""
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel("本日のタスク編集")
        title_label.setFont(self.fonts["header"])
        header_layout.addWidget(title_label)
        
        # Exception checkbox
        self.exception_checkbox = QCheckBox("例外を表示")
        self.exception_checkbox.setChecked(self.show_exceptions)
        self.exception_checkbox.stateChanged.connect(self.toggle_exceptions)
        header_layout.addWidget(self.exception_checkbox)
        
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)
    
    def build_content(self):
        """Build the main content section with task table"""
        # Task table
        self.task_table = QTableWidget()
        self.task_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.task_table.setSelectionMode(QTableWidget.SingleSelection)
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["タスク名", "状態", "曜日", "タグ", "詳細"])
        self.task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.main_layout.addWidget(self.task_table)
        
        # Add task form (initially hidden)
        self.add_form_group = QGroupBox("新しいタスク")
        self.add_form_layout = QVBoxLayout(self.add_form_group)
        
        # Task name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("タスク名:"))
        self.task_name_edit = QLineEdit()
        name_layout.addWidget(self.task_name_edit)
        self.add_form_layout.addLayout(name_layout)
        
        # Status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("状態:"))
        self.status_combo = QComboBox()
        self.status_combo.addItems(["working", "planned", "closed"])
        status_layout.addWidget(self.status_combo)
        self.add_form_layout.addLayout(status_layout)
        
        # Days
        days_layout = QHBoxLayout()
        days_layout.addWidget(QLabel("曜日:"))
        self.day_checkboxes = {}
        
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Free"]:
            checkbox = QCheckBox(day)
            if day == "Free" or day == datetime.now().strftime("%A"):
                checkbox.setChecked(True)
            days_layout.addWidget(checkbox)
            self.day_checkboxes[day] = checkbox
        
        self.add_form_layout.addLayout(days_layout)
        
        # Tags
        tags_layout = QHBoxLayout()
        tags_layout.addWidget(QLabel("タグ:"))
        self.tags_combo = QComboBox()
        tags_layout.addWidget(self.tags_combo)
        self.add_form_layout.addLayout(tags_layout)
        
        # Task details
        details_layout = QHBoxLayout()
        details_layout.addWidget(QLabel("詳細:"))
        self.details_edit = QTextEdit()
        details_layout.addWidget(self.details_edit)
        self.add_form_layout.addLayout(details_layout)
        
        # Add task button
        add_button_layout = QHBoxLayout()
        add_task_button = QPushButton("追加")
        add_task_button.clicked.connect(self.add_new_task)
        add_button_layout.addWidget(add_task_button)
        
        cancel_add_button = QPushButton("キャンセル")
        cancel_add_button.clicked.connect(self.toggle_add_form)
        add_button_layout.addWidget(cancel_add_button)
        
        self.add_form_layout.addLayout(add_button_layout)
        
        # Hide form initially
        self.add_form_group.setVisible(False)
        self.main_layout.addWidget(self.add_form_group)
    
    def build_footer(self):
        """Build the footer section with action buttons"""
        button_layout = QHBoxLayout()
        
        # Add button
        add_button = QPushButton("追加")
        add_button.clicked.connect(self.toggle_add_form)
        button_layout.addWidget(add_button)
        
        # Delete button
        delete_button = QPushButton("削除")
        delete_button.clicked.connect(self.delete_selected_task)
        button_layout.addWidget(delete_button)
        
        # Save button
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_tasks)
        button_layout.addWidget(save_button)
        
        # Close button
        close_button = QPushButton("閉じる")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)
        
        button_layout.addStretch()
        self.main_layout.addLayout(button_layout)
    
    def update_task_table(self):
        """Update the task table with current tasks"""
        self.task_table.setRowCount(0)  # Clear existing rows
        
        # Filter tasks based on today's day or exceptions
        filtered_tasks = self.filter_today_tasks()
        
        # Update tags combo box with available tags
        self.update_tags_combo()
        
        for idx, task in enumerate(filtered_tasks):
            self.task_table.insertRow(idx)
            
            # Task name
            name_item = QTableWidgetItem(task.name)
            self.task_table.setItem(idx, 0, name_item)
            
            # Status
            status_item = QTableWidgetItem(task.status)
            self.task_table.setItem(idx, 1, status_item)
            
            # Days
            days_item = QTableWidgetItem(", ".join(task.days))
            self.task_table.setItem(idx, 2, days_item)
            
            # Tags
            tags_item = QTableWidgetItem(", ".join(task.tags))
            self.task_table.setItem(idx, 3, tags_item)
            
            # Details
            details_item = QTableWidgetItem(task.details)
            self.task_table.setItem(idx, 4, details_item)
    
    def filter_today_tasks(self):
        """Filter tasks based on whether they're for today or exceptions are allowed"""
        if self.show_exceptions:
            return self.tasks
        else:
            today = datetime.now().strftime("%A")
            return [task for task in self.tasks if today in task.days or "Free" in task.days]
    
    def update_tags_combo(self):
        """Update the tags combo box with available tags"""
        current_text = self.tags_combo.currentText() if self.tags_combo.count() > 0 else ""
        
        self.tags_combo.clear()
        self.tags_combo.addItems(self.all_tags)
        
        # Try to restore previous selection
        index = self.tags_combo.findText(current_text)
        if index >= 0:
            self.tags_combo.setCurrentIndex(index)
    
    def toggle_exceptions(self, state):
        """Toggle showing exception tasks"""
        self.show_exceptions = (state == Qt.Checked)
        self.update_task_table()
    
    def toggle_add_form(self):
        """Toggle visibility of add task form"""
        self.add_form_visible = not self.add_form_visible
        self.add_form_group.setVisible(self.add_form_visible)
        
        if self.add_form_visible:
            # Reset form fields
            self.task_name_edit.clear()
            self.status_combo.setCurrentIndex(1)  # Default to "planned"
            self.details_edit.clear()
            
            # Set today and Free as checked by default
            today = datetime.now().strftime("%A")
            for day, checkbox in self.day_checkboxes.items():
                checkbox.setChecked(day == "Free" or day == today)
    
    def add_new_task(self):
        """Add a new task based on form input"""
        if not self.controller:
            return
        
        # Get task name
        task_name = self.task_name_edit.text().strip()
        if not task_name:
            QMessageBox.warning(self, "Warning", "タスク名を入力してください。")
            return
        
        # Get selected days
        selected_days = [day for day, checkbox in self.day_checkboxes.items() if checkbox.isChecked()]
        if not selected_days:
            selected_days = ["Free"]  # Default to Free if none selected
        
        # Get selected tag
        selected_tag = self.tags_combo.currentText()
        
        # Create new task
        new_task = self.controller.create_new_task(
            name=task_name,
            status=self.status_combo.currentText(),
            days=selected_days,
            details=self.details_edit.toPlainText(),
            tags=[selected_tag] if selected_tag else []
        )
        
        # Add to model via controller
        self.controller.add_task(new_task)
        
        # Update UI
        self.toggle_add_form()
        self.set_tasks(self.controller.get_filtered_tasks())
    
    def delete_selected_task(self):
        """Delete the selected task"""
        selected_rows = self.task_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "タスクを選択してください。")
            return
        
        row = selected_rows[0].row()
        filtered_tasks = self.filter_today_tasks()
        
        if row < 0 or row >= len(filtered_tasks):
            return
        
        # Confirm deletion
        task = filtered_tasks[row]
        confirm = QMessageBox.question(
            self, 
            "Confirm", 
            f"タスク「{task.name}」を削除しますか？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes and self.controller:
            self.controller.delete_task(task)
            self.set_tasks(self.controller.get_filtered_tasks())
    
    def save_tasks(self):
        """Save all tasks"""
        if self.controller and self.controller.save_tasks():
            QMessageBox.information(self, "Success", "タスクが保存されました。")
