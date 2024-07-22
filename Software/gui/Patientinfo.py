import os
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QLineEdit, QPushButton, QLabel, QDateTimeEdit, QComboBox, QHeaderView)
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import Qt
from datetime import datetime
import json

class PatientInfoWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Access Patient Data')
        self.resize(1200, 900)
        self.center()  

        # Layouts
        mainLayout = QVBoxLayout()
        filterLayout = QHBoxLayout()
        BackLayout = QVBoxLayout()

        # Filter inputs
        self.nameFilter = QLineEdit(self)
        self.nameFilter.setPlaceholderText("Search by name")
        filterLayout.addWidget(self.nameFilter)

        # Dropdown for diagnosis filter
        self.diagnosisFilter = QComboBox(self)
        self.diagnosisFilter.addItems(["", "No COVID or pneumonia detected",
                                        "Pneumonia - likely viral infection", 
                                        "COVID-19 detected, immediate action required", 
                                        "Healthy - No abnormalies detected in lungs", 
                                        "Pneumonia - likely bacterial infection"])
        self.diagnosisFilter.currentIndexChanged.connect(self.filter_results)  # Connect to filter function
        filterLayout.addWidget(self.diagnosisFilter)

        self.timeFilter = QDateTimeEdit(self)
        self.timeFilter.setCalendarPopup(True)
        self.timeFilter.setDisplayFormat("yyyy-MM-dd")
        self.timeFilter.dateTimeChanged.connect(self.filter_results)
        self.timeFilter.setDateTime(QDateTime.currentDateTime())   
        filterLayout.addWidget(self.timeFilter)

        self.searchButton = QPushButton('Search', self)
        self.searchButton.clicked.connect(self.filter_results)
        filterLayout.addWidget(self.searchButton)

        self.clearButton = QPushButton('Clear Filters', self)
        self.clearButton.clicked.connect(self.load_data)
        filterLayout.addWidget(self.clearButton)

        # Table to display patients
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)  
        self.table.setHorizontalHeaderLabels(['Name', 'Diagnosis', 'Date', 'Time'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        mainLayout.addLayout(filterLayout)
        mainLayout.addWidget(self.table)


        self.setLayout(mainLayout)
        self.load_data()
    
    def center(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def load_data(self):
        metadata_file = 'data/patientinfo.json'
        try:
            with open(metadata_file, 'r') as file:
                data = json.load(file)
            self.display_data(data)
        except Exception as e:
            QMessageBox.warning(self, "Load Error", f"Failed to load data: {str(e)}")

    def display_data(self, data):
        self.table.setRowCount(len(data))
        for i, entry in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(entry['patient_name']))
            self.table.setItem(i, 1, QTableWidgetItem(entry['diagnosis']))
            date_time = datetime.fromisoformat(entry['timestamp'])
            self.table.setItem(i, 2, QTableWidgetItem(date_time.strftime("%Y-%m-%d")))
            self.table.setItem(i, 3, QTableWidgetItem(date_time.strftime("%H:%M:%S")))

            delete_button = QPushButton('Delete')
            delete_button.clicked.connect(lambda ch, row=i: self.delete_entry(row))
            self.table.setCellWidget(i, 4, delete_button)

    def delete_entry(self, row):
        metadata_file = 'data/patientinfo.json'
        try:
            with open(metadata_file, 'r') as file:
                data = json.load(file)
            data.pop(row)
            with open(metadata_file, 'w') as file:
                json.dump(data, file, indent=4)
            self.load_data()  # Refresh the table
        except Exception as e:
            QMessageBox.warning(self, "Delete Error", f"Failed to delete data: {str(e)}")


    def filter_results(self):
        metadata_file = 'data/patientinfo.json'
        try:
            with open(metadata_file, 'r') as file:
                data = json.load(file)
            if self.nameFilter.text():
                data = [entry for entry in data if self.nameFilter.text().lower() in entry['patient_name'].lower()]
            if self.diagnosisFilter.currentText():
                data = [entry for entry in data if self.diagnosisFilter.currentText() == entry['diagnosis']]
            if self.timeFilter.dateTime().toString("yyyy-MM-dd"):
                selected_date = self.timeFilter.dateTime().toString("yyyy-MM-dd")
                data = [entry for entry in data if datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d") == selected_date]
            self.display_data(data)
        except Exception as e:
            QMessageBox.warning(self, "comfirm access?", f"Opening data")

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PatientInfoWindow()
    ex.show()
    sys.exit(app.exec_())
