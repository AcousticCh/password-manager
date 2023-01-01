from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox, QTreeWidget, QTreeView
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QColor

import sys
import json 
import random
import pyperclip


class StandardItem(QStandardItem):
    def __init__(self, text="", font_size=12, set_bold=False, color=QColor(255, 255, 255)):
        super().__init__()

        font = QFont("Open Sans", font_size)
        font.setBold(set_bold)

        self.setEditable(False)
        self.setForeground(color)
        self.setFont(font)
        self.setText(text)


# create QMainWindow subclass
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tree_model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.tree_model)
        self.load()
        
        self.root_node = self.tree_model.invisibleRootItem()
        america = StandardItem("America", 16, set_bold=True)
        california = StandardItem("California", 14)
        america.appendRow(california)

        oakland = StandardItem("Oakland")
        sanfrancisco = StandardItem("San Fancisco")
        sanjose = StandardItem("San Jose")

        california.appendRow(oakland)
        california.appendRow(sanfrancisco)
        california.appendRow(sanjose)

        self.root_node.appendRow(america)
        self.tree_view.expandAll()

        # UI SETUP
        # WINDOW SETUP
        self.setWindowTitle("Password Manager")
        self.setMinimumSize(QSize(400, 200))
        
        # WIDGET CREATION/SETUP

        # Views
        # self.accountView = QListView()
        # self.accountView.setObjectName(u"accountView")
        # self.accountView.setSelectionMode(QAbstractItemView.SingleSelection)
        # self.accountView.setModel(self.model)

        

        # Labels
        self.website_label = QLabel("Website: ")
        self.email_label = QLabel("Email: ")
        self.username_label = QLabel("Username: ")
        self.password_label = QLabel("Password: ")

        # Inputs
        self.website_input = QLineEdit()
        self.email_input = QLineEdit()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()

        # Buttons
        self.search_button = QPushButton("Search")
        self.generate_password_button = QPushButton("Generate Password")
        self.add_entry_button = QPushButton("Add Account")
        self.delete_button = QPushButton("Delete Account")

        # LAYOUT
        layout = QVBoxLayout()

        row0 = QHBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()
        row5 = QHBoxLayout()
        row6 = QHBoxLayout()


        row0.addWidget(self.tree_view)

        row1.addWidget(self.website_label)
        row1.addWidget(self.website_input)
        

        row2.addWidget(self.email_label)
        row2.addWidget(self.email_input)

        row3.addWidget(self.username_label)
        row3.addWidget(self.username_input)

        row4.addWidget(self.password_label)
        row4.addWidget(self.password_input)
        

        row5.addWidget(self.search_button)
        row5.addWidget(self.generate_password_button)

        row6.addWidget(self.add_entry_button)
        row6.addWidget(self.delete_button)

        layout.addLayout(row0)
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)
        layout.addLayout(row5)
        layout.addLayout(row6)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

        # Button Signals
        self.add_entry_button.pressed.connect(self.add)
        self.delete_button.pressed.connect(self.delete)
        self.generate_password_button.pressed.connect(self.generate_password)

    def add(self):
        website = self.website_input.text()
        username = {"username": self.username_input.text()}

        account = { 
            website: {
                        "username" : self.username_input.text(),
                        "email": self.email_input.text(),
                        "password": self.password_input.text()
                    }
        }

        if website:
            self.root_node.appendRow()
            self.tree_model.layoutChanged.emit()
            self.website_input.setText("")
            self.email_input.setText("")
            self.username_input.setText("")
            self.password_input.setText("")
            self.save()

    def delete(self):
        indexes = self.accountView.selectedIndexes()
        if indexes:
            index = indexes[0]
            del self.model.accounts[index.row()]
            self.model.layoutChanged.emit()
            self.accountView.clearSelection()
            # self.save()

    def generate_password(self):
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        nr_letters = random.randint(8, 10)
        nr_symbols = random.randint(2, 4)
        nr_numbers = random.randint(2, 4)

        letter_list = [random.choice(letters) for char in range(nr_letters)]
        symbol_list = [random.choice(symbols) for char in range(nr_symbols)]
        number_list = [random.choice(numbers) for char in range(nr_numbers)]
        password_list = letter_list + symbol_list + number_list

        random.shuffle(password_list)

        password = "".join(password_list)
        self.password_input.setText(password)
        pyperclip.copy(password)
        copy_message = QMessageBox()
        copy_message.setText("Password is copied to clipboard")
        copy_message.exec()


    def save(self):
        with open("data.json") as file:
            data = json.dump(self.root_node)

    def load(self):
        try:
            pass

        except Exception:
            pass



app = QApplication(sys.argv)




window = MainWindow()
window.show() # root windows with no parent are hidden by default

app.exec() # begins event loop