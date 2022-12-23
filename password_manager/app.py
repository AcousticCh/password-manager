from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout, QListView, QAbstractItemView
from PySide6.QtCore import QSize, Qt
from PySide6 import QtCore
import sys
import json 
class CredModel(QtCore.QAbstractListModel):
    def __init__(self, *args, accounts=None, **kwargs):
        super(CredModel, self).__init__(*args, **kwargs)
        self.accounts = accounts or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            _, account = self.accounts[index.row()]
            return account

    def rowCount(self, index):
        return len(self.accounts)

# create QMainWindow subclass
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = CredModel()
        self.load()
        

        # UI SETUP
        # WINDOW SETUP
        self.setWindowTitle("Password Manager")
        self.setMinimumSize(QSize(400, 200))
        
        # WIDGET CREATION/SETUP

        # Views
        self.accountView = QListView()
        self.accountView.setObjectName(u"accountView")
        self.accountView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.accountView.setModel(self.model)

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

        row0 = QHBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()


        row0.addWidget(self.accountView)

        row1.addWidget(self.website_label)
        row1.addWidget(self.website_input)
        row1.addWidget(self.search_button)

        row2.addWidget(self.email_label)
        row2.addWidget(self.email_input)

        row3.addWidget(self.password_label)
        row3.addWidget(self.password_input)
        row3.addWidget(self.generate_password_button)

        row4.addWidget(self.add_entry_button)

        layout.addLayout(row0)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        # Button Signals
        self.add_entry_button.pressed.connect(self.add)

    def add(self):
        account = f"{self.website_input.text()}, {self.email_input.text()}, {self.password_input.text()}"
        if account:
            self.model.accounts.append((False, account))
            self.model.layoutChanged.emit()
            self.website_input.setText("")
            self.email_input.setText("")
            self.password_input.setText("")
            self.save()


    def save(self):
        with open("data.json", "w") as file:
            data = json.dump(self.model.accounts, file)

    def load(self):
        try:
            with open("data.json", "r") as file:
                self.model.accounts = json.load(file)
        except Exception:
            pass

app = QApplication(sys.argv)

window = MainWindow()
window.show() # root windows with no parent are hidden by default

app.exec() # begins event loop