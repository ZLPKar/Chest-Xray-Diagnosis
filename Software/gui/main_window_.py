from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFile, QTextStream
from gui.diagnosis import DiagnoseWindow
from gui.Patientinfo import PatientInfoWindow
from gui.coviddetector import CovidDetectorWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.resize(1200, 800)
        self.center()

        self.loadStyleSheet('resources/styles/Main.qss')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        

        self.btn_detect = QPushButton('Detect Covid 19', self)
        self.btn_detect.clicked.connect(self.open_covid_detector)
        
        layout.addWidget(self.btn_detect)

        self.btn_diagnose = QPushButton('Diagnose for Pnuemonia', self)
        self.btn_diagnose.clicked.connect(self.open_diagnose_page)
         
        layout.addWidget(self.btn_diagnose)

        self.btn_access = QPushButton('Access Patient Database', self)
        self.btn_access.clicked.connect(self.open_access_page)
        
        layout.addWidget(self.btn_access)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def loadStyleSheet(self, path):
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def open_covid_detector(self):
        self.covid_window = CovidDetectorWindow(self)
        self.covid_window.show()
        self.close()

    def open_diagnose_page(self):
        self.diagnose_window = DiagnoseWindow(self)
        self.diagnose_window.show()
        self.close()

    def open_access_page(self):
        self.patient_info_window = PatientInfoWindow(self)
        self.patient_info_window.show()
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
