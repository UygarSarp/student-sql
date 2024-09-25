from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QComboBox, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout
import sys
import sqlite3
from PyQt6.QtGui import QAction


class MainWinow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management")

        file_menu = self.menuBar().addMenu("&File")
        about_menu = self.menuBar().addMenu("&About")
        edit_menu = self.menuBar().addMenu("&Edit")

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert_add)
        file_menu.addAction(add_student_action)

        search_action = QAction("Search", self)
        search_action.triggered.connect(self.insert_search)
        edit_menu.addAction(search_action)

        about_action = QAction("About", self)
        about_menu.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        veri = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row in enumerate(veri):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert_add(self):
        dialog = InsertAddDialog()
        dialog.exec()

    def insert_search(self):
        dialog = InsertSearchDialog()
        dialog.exec()


class InsertAddDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        self.course = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course.addItems(courses)
        layout.addWidget(self.course)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        button = QPushButton("Insert")
        button.pressed.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.name.text()
        course = self.course.itemText(self.course.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?,?,?)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()

        main_window.load_data()


class InsertSearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.name = QLineEdit()
        self.name.setPlaceholderText("Name")
        layout.addWidget(self.name)

        button = QPushButton("Search")
        button.pressed.connect(self.search)
        layout.addWidget(button)

        self.setLayout(layout)

    def search(self):
        name = self.name
        name = name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))
        rows = list(result)
        print(rows)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWinow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())