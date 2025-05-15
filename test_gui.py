import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
)
from PySide6.QtCore import QTimer


class DynamixelMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dynamixel Data Viewer")
        self.resize(600, 300)

     
        layout = QVBoxLayout()
        self.setLayout(layout)

       
        layout.addWidget(QLabel("Live Dynamixel Data"))

        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Baud Rate", "Return Delay Time", "Temperature Limit", "Moving"])
        layout.addWidget(self.table)

      
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(500)

    def update_data(self):
     
        dynamixel_data = get_dynamixel_data()

        self.table.setRowCount(len(dynamixel_data))

        for row, (dxl_id, position, velocity, temp, moving) in enumerate(dynamixel_data):
            self.table.setItem(row, 0, QTableWidgetItem(str(dxl_id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(position)))
            self.table.setItem(row, 2, QTableWidgetItem(str(velocity)))
            self.table.setItem(row, 3, QTableWidgetItem(str(temp)))
            self.table.setItem(row, 4, QTableWidgetItem(str(moving)))



def get_dynamixel_data():
    
    data1 = Read(descr, 4, 4, 1)
    data2 = Read(descr, 4, 5, 1)
    data3 = Read(descr, 4, 11, 1)
    data4 = Read(descr, 4, 46, 1)
    return [(4, data1[5], data2[5], data3[5], data4[5]), ("no data", "no data", "no data", "no data", "no data"), ("no data", "no data", "no data", "no data", "no data")]


from low_level import *
import time
descr = open_connection('/dev/ttyAMA0', 921600)
if descr == -1:
    print("OPEN error")
    exit()

app = QApplication(sys.argv)
window = DynamixelMonitor()
window.show()
sys.exit(app.exec())