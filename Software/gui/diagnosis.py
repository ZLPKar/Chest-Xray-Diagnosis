import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,  QLabel, QLineEdit, QFileDialog, QMessageBox, QApplication, QDesktopWidget)
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtCore import Qt, QFile, QTextStream
import numpy as np
import os
from model.load_model import get_model1
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import json
from datetime import datetime


class DiagnoseWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.model = get_model1()
        self.imagePath = None  
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pneumonia diagnosis')
        self.resize(1200, 900)
        self.center()
        self.loadStyleSheet('resources/styles/diagnose.qss')

        layout = QVBoxLayout(self)

        self.uploadButton = QPushButton('Upload X-ray Image')
        self.uploadButton.clicked.connect(self.openFileDialog)
        layout.addWidget(self.uploadButton)

        # Container for the image and its label
        imageLayout = QVBoxLayout()
        imageLayout.setAlignment(Qt.AlignCenter)  # Center the image

        self.imageLabel = QLabel('No image loaded')
        self.imageLabel.setAlignment(Qt.AlignCenter)  
        self.imageLabel.setFixedSize(300, 300)  
        imageLayout.addWidget(self.imageLabel)

        self.imageNameLabel = QLabel('')  # Label for displaying the image name
        self.imageNameLabel.setAlignment(Qt.AlignCenter)  
        imageLayout.addWidget(self.imageNameLabel)

        layout.addLayout(imageLayout)  

        self.nameLabel = QLabel('Key in Patient Name:')
        layout.addWidget(self.nameLabel)

        self.nameEdit = QLineEdit()
        self.nameEdit.textChanged.connect(self.enableDiagnoseButton)
        layout.addWidget(self.nameEdit)

        self.diagnoseButton = QPushButton('Start Diagnosis')
        self.diagnoseButton.clicked.connect(self.diagnose)
        self.diagnoseButton.setEnabled(False)
        layout.addWidget(self.diagnoseButton)

        self.resultLabel = QLabel('Diagnosis will appear here')
        layout.addWidget(self.resultLabel)

        self.backButton = QPushButton('Back')
        self.backButton.clicked.connect(self.goBack)
        layout.addWidget(self.backButton)

        self.setLayout(layout)

    def center(self):
        screen = QGuiApplication.primaryScreen().geometry()
        window_geometry = self.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
    
    def loadStyleSheet(self, path):
        file = QFile(path)
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if fileName:
            self.imagePath = fileName
            self.displayImage(fileName)
            self.imageNameLabel.setText(os.path.basename(fileName))  # Display the file name
            self.enableDiagnoseButton()

    def displayImage(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.imageLabel.setPixmap(pixmap)
        else:
            QMessageBox.warning(self, "Image Load Error", "The image file could not be loaded. Please select a valid image file.")

    def enableDiagnoseButton(self):
        if self.imagePath and self.nameEdit.text().strip():
            self.diagnoseButton.setEnabled(True)
        else:
            self.diagnoseButton.setEnabled(False)

    def diagnose(self):
        if self.imagePath and self.nameEdit.text().strip():
            img = image.load_img(self.imagePath, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            img_array = img_array / 255.0

            preds = self.model.predict(img_array)
            predicted_class = np.argmax(preds, axis=1)[0]

            diagnosis_messages = {
                0: 'Pneumonia - likely bacterial infection',
                1: 'Healthy - No abnormalies detected in lungs',
                2: 'Pneumonia - likely viral infection'
            }

            diagnosis = diagnosis_messages[predicted_class]
            self.resultLabel.setText(f'Patient: {self.nameEdit.text()} \nDiagnosis: {diagnosis}')
            self.saveMetadata(self.imagePath, self.nameEdit.text(), diagnosis, datetime.now().isoformat())
        else:
            QMessageBox.warning(self, 'Error', 'Please upload an image and enter the patient name before diagnosing.')
            

    def saveMetadata(self, imagePath, patientName, diagnosis, timestamp):
        metadata_file = 'data/patientinfo.json'
        new_entry = {
            'filename': os.path.basename(imagePath),
            'patient_name': patientName,
            'diagnosis': diagnosis,
            'timestamp': timestamp
        }

        try:
            # Check if the file exists and has content
            if os.path.exists(metadata_file) and os.path.getsize(metadata_file) > 0:
                with open(metadata_file, 'r+') as file:
                    try:
                        # Try loading the existing data as JSON
                        data = json.load(file)
                        if isinstance(data, dict):  # If data is a dictionary (incorrect format)
                            data = [data]  # Convert it into a list
                        data.append(new_entry)  
                    except json.JSONDecodeError:
                        data = [new_entry]  
                    file.seek(0)  
                    json.dump(data, file, indent=4)  
                    file.truncate()  
            else:
                
                with open(metadata_file, 'w') as file:
                    json.dump([new_entry], file, indent=4)  
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save metadata: {str(e)}")


    def goBack(self):
        self.close()
        self.main_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DiagnoseWindow(None)
    ex.show()
    sys.exit(app.exec_())
