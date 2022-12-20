from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout
from PySide6.QtCore import QSize
import sys

# create QMainWindow subclass
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # WINDOW SETUP
        self.setWindowTitle("Password Manager")
        self.setMinimumSize(QSize(400, 200))
        
        # WIDGET CREATION/SETUP

        # Labels
        self.website_label = QLabel("Website: ")
        self.email_label = QLabel("Email/Username: ")
        self.password_label = QLabel("Password: ")

        # Inputs
        self.website_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()

        # Buttons
        self.search_button = QPushButton("Search")
        self.generate_password_button = QPushButton("Generate Password")
        self.add_entry_button = QPushButton("Add Account")

        # LAYOUT
        layout = QVBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()


        row1.addWidget(self.website_label)
        row1.addWidget(self.website_input)
        row1.addWidget(self.search_button)

        row2.addWidget(self.email_label)
        row2.addWidget(self.email_input)

        row3.addWidget(self.password_label)
        row3.addWidget(self.password_input)
        row3.addWidget(self.generate_password_button)

        row4.addWidget(self.add_entry_button)

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show() # root windows with no parent are hidden by default

app.exec() # begins event loop