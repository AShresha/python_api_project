import sys
from aggregation_function import run_analysis

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel
)

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Data Aggregation Tool")

        layout = QVBoxLayout()

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter token")

        self.station_input = QLineEdit()
        self.station_input.setPlaceholderText("Enter station number")

        self.param_input = QLineEdit()
        self.param_input.setPlaceholderText("Enter parameter IDs (comma separated)")

        self.run_button = QPushButton("Run Analysis")
        self.result_box = QTextEdit()

        layout.addWidget(QLabel("Token"))
        layout.addWidget(self.token_input)

        layout.addWidget(QLabel("Station"))
        layout.addWidget(self.station_input)

        layout.addWidget(QLabel("Parameters"))
        layout.addWidget(self.param_input)

        layout.addWidget(self.run_button)
        layout.addWidget(self.result_box)

        self.setLayout(layout)

        self.run_button.clicked.connect(self.run)

    def run(self):
        token = self.token_input.text()
        station = int(self.station_input.text())
        params = [int(x.strip()) for x in self.param_input.text().split(",")]

        # call your logic function here
        result = run_analysis(
            token,
            station,
            params,
            "2025-12-25T00:00:00",
            "2025-12-25T10:00:00"
        )

        self.result_box.setText(str(result))


app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())