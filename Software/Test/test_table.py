import sys
from PyQt5.QtWidgets import QApplication
from gui.Patientinfo import PatientInfoWindow
import unittest

class TestPatientInfoWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = PatientInfoWindow(None)

    def test_load_data(self):
        
        self.window.load_data()
        # Check if the table has rows populated
        self.assertGreater(self.window.table.rowCount(), 0)