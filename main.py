import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("./main.ui", self)

        self.con = sqlite3.connect("coffee.sqlite")

        cursor = self.con.cursor()
        data = cursor.execute("SELECT * FROM coffee").fetchall()

        headers = [
            "ID",
            "Название сорта",
            "Степень обжарки",
            "Молотый/в зернах",
            "Описание вкуса",
            "Цена",
            "Объем упаковки"
        ]

        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)

        for row in data:
            items = [QStandardItem(str(value)) for value in row]
            model.appendRow(items)

        self.tableView.setModel(model)

        self.tableView.resizeColumnsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())