from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QLineEdit, QHBoxLayout, QWidget, QVBoxLayout, QMessageBox, QTreeWidget, QTreeView
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem, QFont, QColor

import sys
import json 
import random
import pyperclip



import json
import sys
from typing import Any, Iterable, List, Dict, Union

from PySide6.QtWidgets import QTreeView, QApplication, QHeaderView
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QObject, Qt, QFileInfo


class TreeItem:
    """A Json item corresponding to a line in QTreeView"""

    def __init__(self, parent: "TreeItem" = None):
        self._parent = parent
        self._key = ""
        self._value = ""
        self._value_type = None
        self._children = []

    def appendChild(self, item: "TreeItem"):
        """Add item as a child"""
        self._children.append(item)

    def child(self, row: int) -> "TreeItem":
        """Return the child of the current item from the given row"""
        return self._children[row]

    def parent(self) -> "TreeItem":
        """Return the parent of the current item"""
        return self._parent

    def childCount(self) -> int:
        """Return the number of children of the current item"""
        return len(self._children)

    def row(self) -> int:
        """Return the row where the current item occupies in the parent"""
        return self._parent._children.index(self) if self._parent else 0

    @property
    def key(self) -> str:
        """Return the key name"""
        return self._key

    @key.setter
    def key(self, key: str):
        """Set key name of the current item"""
        self._key = key

    @property
    def value(self) -> str:
        """Return the value name of the current item"""
        return self._value

    @value.setter
    def value(self, value: str):
        """Set value name of the current item"""
        self._value = value

    @property
    def value_type(self):
        """Return the python type of the item's value."""
        return self._value_type

    @value_type.setter
    def value_type(self, value):
        """Set the python type of the item's value."""
        self._value_type = value

    @classmethod
    def load(
        cls, value: Union[List, Dict], parent: "TreeItem" = None, sort=True
    ) -> "TreeItem":
        """Create a 'root' TreeItem from a nested list or a nested dictonary

        Examples:
            with open("file.json") as file:
                data = json.dump(file)
                root = TreeItem.load(data)

        This method is a recursive function that calls itself.

        Returns:
            TreeItem: TreeItem
        """
        rootItem = TreeItem(parent)
        rootItem.key = "root"

        if isinstance(value, dict):
            items = sorted(value.items()) if sort else value.items()

            for key, value in items:
                child = cls.load(value, rootItem)
                child.key = key
                child.value_type = type(value)
                rootItem.appendChild(child)

        elif isinstance(value, list):
            for index, value in enumerate(value):
                child = cls.load(value, rootItem)
                child.key = index
                child.value_type = type(value)
                rootItem.appendChild(child)

        else:
            rootItem.value = value
            rootItem.value_type = type(value)

        return rootItem


class JsonModel(QAbstractItemModel):
    """ An editable model of Json data """

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self._rootItem = TreeItem()
        self._headers = ("key", "value")

    def clear(self):
        """ Clear data from the model """
        self.load({})

    def load(self, document: dict):
        """Load model from a nested dictionary returned by json.loads()

        Arguments:
            document (dict): JSON-compatible dictionary
        """

        assert isinstance(
            document, (dict, list, tuple)
        ), "`document` must be of dict, list or tuple, " f"not {type(document)}"

        self.beginResetModel()

        self._rootItem = TreeItem.load(document)
        self._rootItem.value_type = type(document)

        self.endResetModel()

        return True

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> Any:
        """Override from QAbstractItemModel

        Return data from a json item according index and role

        """
        if not index.isValid():
            return None

        item = index.internalPointer()

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return item.key

            if index.column() == 1:
                return item.value

        elif role == Qt.EditRole:
            if index.column() == 1:
                return item.value

    def setData(self, index: QModelIndex, value: Any, role: Qt.ItemDataRole):
        """Override from QAbstractItemModel

        Set json item according index and role

        Args:
            index (QModelIndex)
            value (Any)
            role (Qt.ItemDataRole)

        """
        if role == Qt.EditRole:
            if index.column() == 1:
                item = index.internalPointer()
                item.value = str(value)

                if __binding__ in ("PySide", "PyQt4"):
                    self.dataChanged.emit(index, index)
                else:
                    self.dataChanged.emit(index, index, [Qt.EditRole])

                return True

        return False

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ):
        """Override from QAbstractItemModel

        For the JsonModel, it returns only data for columns (orientation = Horizontal)

        """
        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:
            return self._headers[section]

    def index(self, row: int, column: int, parent=QModelIndex()) -> QModelIndex:
        """Override from QAbstractItemModel

        Return index according row, column and parent

        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        """Override from QAbstractItemModel

        Return parent index of index

        """

        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=QModelIndex()):
        """Override from QAbstractItemModel

        Return row count from parent index
        """
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent=QModelIndex()):
        """Override from QAbstractItemModel

        Return column number. For the model, it always return 2 columns
        """
        return 2

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """Override from QAbstractItemModel

        Return flags of index
        """
        flags = super(JsonModel, self).flags(index)

        if index.column() == 1:
            return Qt.ItemIsEditable | flags
        else:
            return flags

    def to_json(self, item=None):

        if item is None:
            item = self._rootItem

        nchild = item.childCount()

        if item.value_type is dict:
            document = {}
            for i in range(nchild):
                ch = item.child(i)
                document[ch.key] = self.to_json(ch)
            return document

        elif item.value_type == list:
            document = []
            for i in range(nchild):
                ch = item.child(i)
                document.append(self.to_json(ch))
            return document

        else:
            return item.value



# create QMainWindow subclass
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tree_model = JsonModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.tree_model)
        
        self.json_path = QFileInfo(__file__).absoluteDir().filePath("example.json")


        with open(self.json_path) as file:
            document = json.load(file)
            self.tree_model.load(document)

        
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

        with open(self.json_path, "r") as file:
            data = json.load(file)

        with open(self.json_path, "w") as file:
            data.update(account)
            document = json.dump(data, file)


        if website:
            self.website_input.setText("")
            self.email_input.setText("")
            self.username_input.setText("")
            self.password_input.setText("")
            # self.save()
            
        with open(self.json_path) as file:
            document = json.load(file)
            self.tree_model.load(document)

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
        pass

    def load(self):
        try:
            pass

        except Exception:
            pass



app = QApplication(sys.argv)




window = MainWindow()
window.show() # root windows with no parent are hidden by default

app.exec() # begins event loop