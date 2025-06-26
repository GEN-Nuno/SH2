from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QPushButton,
                            QLabel, QGroupBox, QHBoxLayout, QTableWidget,
                            QTableWidgetItem, QComboBox, QSpinBox, QCheckBox,
                            QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, QDate, QTimer
import locale
from datetime import datetime

class MainView(QMainWindow):
    """Main view of the scheduler application"""
    
    def __init__(self, theme_factory):
        super().__init__()
        self.theme_factory = theme_factory
        self.colors = theme_factory.create_color_scheme()
        self.fonts = theme_factory.create_font_scheme()
        self.setStyleSheet(theme_factory.create_style_sheet())
        
        self.setWindowTitle("Task Scheduler")
        self.setMinimumSize(800, 600)
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Initialize UI components
        self.today_task_button = None
        self.all_schedule_button = None
        self.calculate_button = None
        self.excel_export_button = None
        self.task_table = None
        self.date_label = None
        
        # Set up timer for date updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_label)
        self.timer.start(3600000)  # Update every hour
    
    def build_header(self):
        """Build the header section with title and navigation buttons"""
        header_layout = QHBoxLayout()
        
        # Date label (top left)
        self.date_label = QLabel()
        self.date_label.setFont(self.fonts["normal"])
        self.update_date_label()  # Set initial date
        header_layout.addWidget(self.date_label)
        
        header_layout.addStretch(1)  # Add stretch to push title to center
        
        # Title
        title_label = QLabel("Task Scheduler")
        title_label.setFont(self.fonts["header"])
        header_layout.addWidget(title_label)
        
        # Navigation buttons
        button_layout = QHBoxLayout()
        
        self.today_task_button = QPushButton("Today's Tasks")
        self.today_task_button.setFont(self.fonts["button"])
        button_layout.addWidget(self.today_task_button)
        
        self.all_schedule_button = QPushButton("All Schedules")
        self.all_schedule_button.setFont(self.fonts["button"])
        button_layout.addWidget(self.all_schedule_button)
        
        header_layout.addStretch(1)  # Add stretch to push buttons to right
        header_layout.addLayout(button_layout)
        self.main_layout.addLayout(header_layout)
    
    def build_content(self):
        """Build the main content section with today's tasks"""
        # Today's tasks group
        tasks_group = QGroupBox("Today's Tasks Window")
        tasks_group.setFont(self.fonts["normal"])
        tasks_layout = QVBoxLayout(tasks_group)
        
        # Task table
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(5)
        self.task_table.setHorizontalHeaderLabels(["Task Name", "Status", "Effort", "Completed", "Details"])
        self.task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        tasks_layout.addWidget(self.task_table)
        
        self.main_layout.addWidget(tasks_group)
    
    def build_footer(self):
        """Build the footer section with action buttons"""
        footer_layout = QHBoxLayout()
        
        # Calculation button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFont(self.fonts["button"])
        self.calculate_button.setEnabled(False)  # 最初は無効
        footer_layout.addWidget(self.calculate_button)
        
        # Excel export button (for future implementation)
        self.excel_export_button = QPushButton("EXCEL Export")
        self.excel_export_button.setFont(self.fonts["button"])
        self.excel_export_button.setEnabled(False)  # Disabled as per requirement
        footer_layout.addWidget(self.excel_export_button)
        
        footer_layout.addStretch()
        self.main_layout.addLayout(footer_layout)
    
    def update_today_tasks(self, tasks):
        """Update the today's tasks table"""
        self.task_table.setRowCount(0)  # Clear existing rows
        
        for idx, task in enumerate(tasks):
            self.task_table.insertRow(idx)
            
            # Task name (not editable)
            name_item = QTableWidgetItem(task.name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.task_table.setItem(idx, 0, name_item)
            
            # Status (dropdown)
            status_combo = QComboBox()
            status_combo.addItems(["Working", "Planned", "Completed"])
            # Map UI labels to internal values
            status_map = {"Working": "working", "Planned": "planned", "Completed": "closed"}
            reverse_map = {"working": "Working", "planned": "Planned", "closed": "Completed"}
            
            status_combo.setCurrentText(reverse_map.get(task.status, "Planned"))
            status_combo.currentTextChanged.connect(
                lambda text, t=task: self.update_task_attribute(t, "status", status_map.get(text, "planned"))
            )
            self.task_table.setCellWidget(idx, 1, status_combo)
            
            # Perceived effort (spinbox)
            effort_spin = QSpinBox()
            effort_spin.setRange(0, 100)
            effort_spin.setValue(task.perceived_effort)
            effort_spin.valueChanged.connect(lambda value, t=task: self.update_task_attribute(t, "perceived_effort", value))
            self.task_table.setCellWidget(idx, 2, effort_spin)
            
            # Completed today (checkbox)
            completed_check = QCheckBox()
            completed_check.setChecked(task.completed_today)
            completed_check.stateChanged.connect(lambda state, t=task: self.update_task_attribute(t, "completed_today", state == Qt.Checked))
            check_widget = QWidget()
            check_layout = QHBoxLayout(check_widget)
            check_layout.addWidget(completed_check)
            check_layout.setAlignment(Qt.AlignCenter)
            check_layout.setContentsMargins(0, 0, 0, 0)
            self.task_table.setCellWidget(idx, 3, check_widget)
            
            # Detail button
            detail_button = QPushButton("Details")
            self.task_table.setCellWidget(idx, 4, detail_button)
            # Connect to show task detail view
            detail_button.clicked.connect(lambda checked, t=task: self.show_task_detail(t))
        
        # 計算ボタンの有効/無効を更新
        self.update_calculate_button(tasks)
    
    def update_task_attribute(self, task, attribute, value):
        """Update a task attribute and notify the model"""
        if hasattr(task, attribute):
            setattr(task, attribute, value)
            if hasattr(self, 'task_detail_controller'):
                self.task_detail_controller.model.notify()
            # Update calculate button state after attribute change
            self.update_calculate_button(self.task_detail_controller.get_filtered_tasks() if hasattr(self, 'task_detail_controller') else [])
    
    def show_task_detail(self, task):
        """Show task detail in a new window"""
        if hasattr(self, 'task_detail_controller'):
            self.task_detail_controller.show_task_detail_view(task, self)
    
    # Remove the Observer.update method and replace with a method the controller can call
    def refresh_view(self, tasks):
        """Refresh the view with the provided tasks"""
        try:
            self.update_today_tasks(tasks)
            # Update calculate button status based on latest tasks
            self.update_calculate_button(tasks)
        except Exception as e:
            print(f"Error in MainView refresh: {e}")
            import traceback
            traceback.print_exc()

    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, "Error", message)

    def update_calculate_button(self, tasks):
        """Update the calculate button based on task completion status"""
        if not tasks:
            self.calculate_button.setEnabled(False)
            self.calculate_button.setToolTip("No tasks for today")
            return
            
        all_completed = all(task.completed_today for task in tasks)
        self.calculate_button.setEnabled(all_completed)
        
        if all_completed:
            self.calculate_button.setToolTip("All tasks are completed, calculation enabled")
        else:
            self.calculate_button.setToolTip("Complete all tasks to enable calculation")
    
    def set_task_detail_controller(self, controller):
        """タスク詳細表示用のコントローラーを設定"""
        self.task_detail_controller = controller

    def update_date_label(self):
        """Update the date label with current date information"""
        today = datetime.now()
        # Format: June 26, 2023 (Monday)
        date_format = today.strftime("%B %d, %Y (%A)")
        
        if self.date_label:
            self.date_label.setText(date_format)
        
        # English to Japanese day-of-week mapping
        dow_map = {
            'Monday': 'Monday',
            'Tuesday': 'Tuesday',
            'Wednesday': 'Wednesday',
            'Thursday': 'Thursday',
            'Friday': 'Friday',
            'Saturday': 'Saturday',
            'Sunday': 'Sunday'
        }
        
        for eng, jpn in dow_map.items():
            date_format = date_format.replace(eng, jpn)
        
        if self.date_label:
            self.date_label.setText(date_format)
