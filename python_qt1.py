import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWinddow, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt, QTimer
from PyQt5.QtGui import QColor

API_URL = "http://127.0.0.1:5000/"

class ResultTableModel(QAbstractTableModel):
    headers = ["Time","Aggregated_value","TSS value","aggregation"]

    def __init__(self):
        super().__init()
        self._data = []

    def rowCount(self, parent = None):
        return len(self._data)
    
    def columnCount(self, parent = None):
        return len(self.headers)
    
    def data(self, index, role = Qt.DisplayRole):
        if not index.isValid():
            return None
        
        row = self._data[index.row()]
        col = index.column()

        if role == Qt.DisplayRole:
            return [
                str(row["time"]),
                row["aggregated_value"],
                row["tss_value"],
                row["aggregation"]
            ][col]
        
        if role == Qt.BackgroundRole and not row["aggregation"]:
            return QColor(255,210,210)
        
        return None
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        
    def update_data(self, new_data):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

class MainWindow(QMainWinddow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aggregation Check")

        self.table = QTableView()
        self.mode1 = ResultTableModel()
        self.table.setModel(self.mode1)
        self.setCentralWidget(self.table)
        self.table.resizeColumnsToContents()

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(5000)

        self.refresh()

    def refresh(self):
        try:
            response = requests.get(API_URL, timeout=5)
            response.raise_for_status()
            self.mode1.update_data(response.json())
        except Exception as 'e':
            print("API error:", a)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(900,400)
    window.show()
    sys.exit(app.exec_())

