import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, QInputDialog, QDesktopWidget
from users.user_management import check_credentials, register_user
from gui.main_window_ import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Welcome to Chest X-ray diagnosis')
        self.resize(600, 500)
        self.center()

        layout = QVBoxLayout()

        logo_label = QLabel(self)
        pixmap = QPixmap('resources/Images/chest xray logo.jpg')  # Ensure the path is correct
        logo_label.setPixmap(pixmap.scaled(350, 350, Qt.KeepAspectRatio))  
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        self.username_label = QLabel('Username:', self)
        self.username_field = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_field)

        self.password_label = QLabel('Password:', self)
        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_field)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        username = self.username_field.text()
        password = self.password_field.text()
        if username == 'admin' and password == 'admin':
            self.register_new_user()
        elif check_credentials(username, password):
            QMessageBox.information(self, 'Login', 'Login successful!')
            self.open_main_window()
        else:
            QMessageBox.warning(self, 'Login', 'Incorrect username or password')

    def register_new_user(self):
        new_username, ok1 = QInputDialog.getText(self, 'Register New User', 'Enter new username:')
        if ok1 and new_username:
            new_password, ok2 = QInputDialog.getText(self, 'Register New User', 'Enter new password:', QLineEdit.Password)
            if ok2 and new_password:
                if register_user(new_username, new_password):
                    QMessageBox.information(self, 'Registration', 'New user registered successfully!')
                else:
                    QMessageBox.warning(self, 'Registration', 'Failed to register user. Username may already exist.')

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

def main():
    app = QApplication(sys.argv)
    ex = LoginWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()