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

        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

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

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()


class InsertDialog(QDialog):
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
        button.pressed.connect(self.add_student())

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


app = QApplication(sys.argv)
main_window = MainWinow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())