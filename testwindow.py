import sys
from PyQt5.QtWidgets import QApplication, QLabel, QTableView

app = QApplication(sys.argv)
label = QLabel("Hello PyQt")
body = QTableView()
label.show()
body.show()
sys.exit(app.exec_())