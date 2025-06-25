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
        
        self.setWindowTitle("本日のタスク編集")
        self.setMinimumSize(800, 600)
        
        # Main layout
        self.main_layout = QVBoxLayout(self)
    
    def set_controller(self, controller):
        """Set the controller for this view"""
        self.controller = controller
        # コントローラーがセットされたら全タスクも取得
        if self.controller:
            self.all_tasks = self.controller.model.tasks
    
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
        self.add_form_group = QGroupBox("タスクの追加")
        self.add_form_layout = QVBoxLayout(self.add_form_group)
        
        # タスク選択用ドロップダウン
        task_selection_layout = QHBoxLayout()
        task_selection_layout.addWidget(QLabel("選択するタスク:"))
        self.task_selection_combo = QComboBox()
        self.task_selection_combo.setMinimumWidth(300)
        task_selection_layout.addWidget(self.task_selection_combo)
        self.add_form_layout.addLayout(task_selection_layout)
        
        # ボタン
        add_button_layout = QHBoxLayout()
        add_task_button = QPushButton("追加")
        add_task_button.clicked.connect(self.add_existing_task)
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
        
        # 全タスクから本日のタスク一覧にないタスクを抽出
        current_task_names = {task.name for task in self.tasks}
        
        # 本日の曜日または例外フラグでフィルタリング
        today = datetime.now().strftime("%A")
        available_tasks = []
        
        for task in self.all_tasks:
            if task.name in current_task_names:
                continue  # 既に追加済みのタスクはスキップ
            
            # 曜日フィルタリング
            if self.show_exceptions or today in task.days or "Free" in task.days:
                available_tasks.append(task)
        
        # タスク名をドロップダウンに追加
        for task in available_tasks:
            days_str = ", ".join(task.days)
            display_text = f"{task.name} ({days_str})"
            self.task_selection_combo.addItem(display_text, task)
    
    def add_existing_task(self):
        """既存タスクを今日のタスクに追加する"""
        if self.task_selection_combo.count() == 0:
            QMessageBox.information(self, "情報", "追加可能なタスクがありません。")
            return
        
        # 選択されたタスクを取得
        selected_index = self.task_selection_combo.currentIndex()
        if selected_index < 0:
            return
            
        selected_task = self.task_selection_combo.itemData(selected_index)
        
        if not selected_task:
            QMessageBox.warning(self, "警告", "タスクが見つかりません。")
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
            QMessageBox.warning(self, "Warning", "タスクを選択してください。")
            return
        
        row = selected_rows[0].row()
        filtered_tasks = self.filter_today_tasks()
        
        if row < 0 or row >= len(filtered_tasks):
            return
        
        # タスク削除（今日のリストから除外するだけ）
        task = filtered_tasks[row]
        confirm = QMessageBox.question(
            self, 
            "確認", 
            f"タスク「{task.name}」を今日のタスクから除外しますか？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.tasks.remove(task)
            self.update_task_table()
            
            # 選択可能なタスクが変わるのでドロップダウン更新
            self.update_task_selection_dropdown()
    
    def save_tasks(self):
        """Save all tasks"""
        if self.controller and self.controller.save_tasks():
            QMessageBox.information(self, "Success", "タスクが保存されました。")