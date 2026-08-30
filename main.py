import os
import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from main_ui import Ui_MainWindow
from addEditCoffeeForm import Ui_AddEditCoffeeForm


if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILE = os.path.join(BASE_DIR, "data", "coffee.sqlite")


class AddEditCoffeeDialog(QDialog):
    def __init__(self, parent=None, coffee=None):
        super().__init__(parent)

        self.ui = Ui_AddEditCoffeeForm()
        self.ui.setupUi(self)

        self.coffee = coffee

        self.ui.roastingComboBox.addItems([
            "Светлая",
            "Средняя",
            "Темная"
        ])

        self.ui.typeComboBox.addItems([
            "В зернах",
            "Молотый"
        ])

        self.ui.saveButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.reject)

        if coffee is not None:
            self.ui.nameEdit.setText(str(coffee[1]))
            self.ui.roastingComboBox.setCurrentText(str(coffee[2]))
            self.ui.typeComboBox.setCurrentText(str(coffee[3]))
            self.ui.tasteEdit.setText(str(coffee[4]))
            self.ui.priceSpinBox.setValue(float(coffee[5]))
            self.ui.volumeSpinBox.setValue(int(coffee[6]))

    def get_data(self):
        return (
            self.ui.nameEdit.text(),
            self.ui.roastingComboBox.currentText(),
            self.ui.typeComboBox.currentText(),
            self.ui.tasteEdit.text(),
            self.ui.priceSpinBox.value(),
            self.ui.volumeSpinBox.value()
        )


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.con = sqlite3.connect(DB_FILE)

        self.ui.addButton.clicked.connect(self.add_coffee)
        self.ui.editButton.clicked.connect(self.edit_coffee)

        self.load_data()

    def load_data(self):
        cursor = self.con.cursor()

        data = cursor.execute(
            "SELECT * FROM coffee ORDER BY id"
        ).fetchall()

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

        self.ui.tableView.setModel(model)
        self.ui.tableView.resizeColumnsToContents()

    def add_coffee(self):
        dialog = AddEditCoffeeDialog(self)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            cursor = self.con.cursor()

            cursor.execute("""
                INSERT INTO coffee
                (name, roasting, type, taste, price, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)

            self.con.commit()
            self.load_data()

    def edit_coffee(self):
        index = self.ui.tableView.currentIndex()

        if not index.isValid():
            return

        row = index.row()

        cursor = self.con.cursor()

        coffee = cursor.execute(
            "SELECT * FROM coffee ORDER BY id"
        ).fetchall()[row]

        dialog = AddEditCoffeeDialog(self, coffee)

        if dialog.exec_() == QDialog.Accepted:
            data = dialog.get_data()

            cursor.execute("""
                UPDATE coffee
                SET name = ?,
                    roasting = ?,
                    type = ?,
                    taste = ?,
                    price = ?,
                    volume = ?
                WHERE id = ?
            """, (*data, coffee[0]))

            self.con.commit()
            self.load_data()

    def closeEvent(self, event):
        self.con.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = MyWidget()
    ex.show()

    sys.exit(app.exec_())