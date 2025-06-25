from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QComboBox, QCheckBox, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scheduler Application")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.task_label = QLabel("本日のタスク")
        layout.addWidget(self.task_label)

        self.task_dropdown = QComboBox()
        layout.addWidget(self.task_dropdown)

        self.edit_task_button = QPushButton("本日のタスク編集")
        self.edit_task_button.clicked.connect(self.edit_task)
        layout.addWidget(self.edit_task_button)

        self.all_schedule_button = QPushButton("全スケジュール")
        self.all_schedule_button.clicked.connect(self.edit_all_schedule)
        layout.addWidget(self.all_schedule_button)

        self.calculate_button = QPushButton("計算")
        self.calculate_button.clicked.connect(self.calculate)
        layout.addWidget(self.calculate_button)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)

    def edit_task(self):
        QMessageBox.information(self, "Edit Task", "本日のタスク編集画面に遷移します。")

    def edit_all_schedule(self):
        QMessageBox.information(self, "Edit All Schedule", "全スケジュール編集画面に遷移します。")

    def calculate(self):
        QMessageBox.information(self, "Calculate", "計算画面を表示します。")