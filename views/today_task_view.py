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
        self.all_tasks = []  # 全タスクを保持する変数を追加
        self.all_tags = []
        self.show_exceptions = False
        self.add_form_visible = False
        
        self.setWindowTitle("Edit Today's Tasks")
        self.setMinimumSize(800, 600)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
    
    def set_controller(self, controller):
        """Set the controller for this view"""
        self.controller = controller
        # Get all tasks through the controller instead of directly from model
        if self.controller:
            self.all_tasks = self.controller.get_all_tasks()

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
        title_label = QLabel("Edit Today's Tasks")
        title_label.setFont(self.fonts["header"])
        header_layout.addWidget(title_label)
        
        # Exception checkbox
        self.exception_checkbox = QCheckBox("Show exceptions (Tasks from other days)")
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
        self.task_table.setHorizontalHeaderLabels(["Task Name", "Status", "Days", "Tags", "Details"])
        self.task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.main_layout.addWidget(self.task_table)
        
        # Add task form (initially hidden)
        self.add_form_group = QGroupBox("Add Task")
        self.add_form_layout = QVBoxLayout(self.add_form_group)
        
        # Task selection dropdown
        task_selection_layout = QHBoxLayout()
        task_selection_layout.addWidget(QLabel("Select Task:"))
        self.task_selection_combo = QComboBox()
        self.task_selection_combo.setMinimumWidth(300)
        task_selection_layout.addWidget(self.task_selection_combo)
        self.add_form_layout.addLayout(task_selection_layout)
        
        # Buttons
        add_button_layout = QHBoxLayout()
        add_task_button = QPushButton("Add")
        add_task_button.clicked.connect(self.add_existing_task)
        add_button_layout.addWidget(add_task_button)
        
        cancel_add_button = QPushButton("Cancel")
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
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.toggle_add_form)
        button_layout.addWidget(add_button)
        
        # Delete button
        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(self.delete_selected_task)
        button_layout.addWidget(delete_button)
        
        # Save button
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_tasks)
        button_layout.addWidget(save_button)
        
        # Close button
        close_button = QPushButton("Close")
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
        if hasattr(self, 'tags_combo') and self.tags_combo.count() > 0:
            current_text = self.tags_combo.currentText()
            
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
        
        # タスク選択ドロップダウンも更新
        if hasattr(self, 'task_selection_combo'):
            self.update_task_selection_dropdown()
    
    def toggle_add_form(self):
        """Toggle visibility of add task form"""
        self.add_form_visible = not self.add_form_visible
        self.add_form_group.setVisible(self.add_form_visible)
        
        if self.add_form_visible:
            # 追加可能なタスクをドロップダウンに表示
            self.update_task_selection_dropdown()
    
    def update_task_selection_dropdown(self):
        """タスク選択ドロップダウンを更新する"""
        self.task_selection_combo.clear()
        
        if not self.controller or not self.all_tasks:
            return
        
        # 全タスクから本日のタスク一覧にないタスクを抽出
        current_task_ids = {id(task) for task in self.tasks}
        
        # 本日の曜日または例外フラグでフィルタリング
        today = datetime.now().strftime("%A")
        available_tasks = []
        
        for task in self.all_tasks:
            if id(task) in current_task_ids:
                continue  # 既に追加済みのタスクはスキップ
            
            # 曜日フィルタリング
            # Free tasks are always available for manual addition regardless of day
            # Other tasks are shown only if they match today's day or exception flag is on
            if "Free" in task.days or (self.show_exceptions or today in task.days):
                available_tasks.append(task)
        
        # タスク名をドロップダウンに追加
        
        for task in available_tasks:
            days_str = ", ".join(task.days)
            display_text = f"{task.name} ({days_str})"
            self.task_selection_combo.addItem(display_text, task)
    
    def add_existing_task(self):
        """Add an existing task to today's tasks"""
        if self.task_selection_combo.count() == 0:
            QMessageBox.information(self, "Information", "No tasks available to add.")
            return
        
        # 選択されたタスクを取得
        selected_index = self.task_selection_combo.currentIndex()
        if selected_index < 0:
            return
            
        selected_task = self.task_selection_combo.itemData(selected_index)
        
        if not selected_task:
            QMessageBox.warning(self, "Warning", "Task not found.")
            return
        
        # 今日のタスクリストに追加
        if selected_task not in self.tasks:
            self.tasks.append(selected_task)
            self.update_task_table()
            self.toggle_add_form()  # フォームを閉じる
            
            # ドロップダウン更新のために選択肢を更新
            self.update_task_selection_dropdown()
    
    def delete_selected_task(self):
        """Delete the selected task"""
        selected_rows = self.task_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "Please select a task.")
            return
        
        row = selected_rows[0].row()
        filtered_tasks = self.filter_today_tasks()
        
        if row < 0 or row >= len(filtered_tasks):
            return
        
        # Ask for confirmation
        task = filtered_tasks[row]
        confirm = QMessageBox.question(
            self, 
            "Confirm", 
            f"Remove task '{task.name}' from today's tasks?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.tasks.remove(task)
            self.update_task_table()
            
            # Notify the controller if available
            if self.controller:
                self.controller.model.notify()
            
            QMessageBox.information(self, "Success", "Task removed.")
            
            # Update dropdown with available tasks
            self.update_task_selection_dropdown()
    
    def save_tasks(self):
        """Save all tasks"""
        if self.controller:
            # First save all tasks (standard behavior)
            self.controller.save_tasks()
            
            # Also save today's tasks specifically with date
            if self.controller.save_today_tasks(self.tasks):
                # No need to directly notify the model - controller will handle it
                QMessageBox.information(self, "Success", "Tasks saved successfully.")