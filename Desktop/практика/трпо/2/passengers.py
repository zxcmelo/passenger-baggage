from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
import sys
class Passenger:
    def __init__(self, name='', flight='', class_type='', weight=''):
        self.name = name
        self.flight = flight
        self.class_type = class_type
        self.weight = weight
    def to_list(self):
        return [self.name, self.flight, self.class_type, self.weight]
    def equals(self, other):
        return self.to_list() == other.to_list()
class PassengerList:
    def __init__(self):
        self.passengers = {}
        self.count = 0
    def add(self, data):
        self.passengers[self.count] = Passenger(*data)
        self.count += 1
    def find_key(self, data):
        target = Passenger(*data)
        for key, passenger in self.passengers.items():
            if passenger.equals(target):
                return key
        return -1
    def delete(self, data):
        key = self.find_key(data)
        if key != -1:
            del self.passengers[key]
            self.count -= 1
    def edit(self, key, data):
        self.passengers[key] = Passenger(*data)
    def load(self, filename):
        self.passengers = {}
        self.count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    parts = [part.strip() for part in line.strip().split(',')]
                    self.add(parts)
    def save(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for passenger in self.passengers.values():
                f.write(", ".join(passenger.to_list()) + "\n")
passengers = PassengerList()
passengers.load("passengers.txt")
app = QtWidgets.QApplication([])
win = uic.loadUi("passengers.ui") 
win.tableWidget.setColumnCount(4)
win.tableWidget.setHorizontalHeaderLabels(["ФИО", "Рейс", "Класс", "Вес багажа (кг)"])
win.tableWidget.setColumnWidth(0, 220)
win.tableWidget.setColumnWidth(1, 100)
win.tableWidget.setColumnWidth(2, 70)
win.tableWidget.setColumnWidth(3, 120)
def load_table():
    win.tableWidget.setRowCount(len(passengers.passengers))
    for row, passenger in enumerate(passengers.passengers.values()):
        for col, val in enumerate(passenger.to_list()):
            win.tableWidget.setItem(row, col, QTableWidgetItem(val))
def add_passenger():
    data = [
        win.lineEdit_name.text(),
        win.lineEdit_flight.text(),
        win.lineEdit_class.text(),
        win.lineEdit_weight.text()
    ]
    passengers.add(data)
    passengers.save("passengers.txt")
    load_table()
def delete_passenger():
    data = [
        win.lineEdit_name.text(),
        win.lineEdit_flight.text(),
        win.lineEdit_class.text(),
        win.lineEdit_weight.text()
    ]
    passengers.delete(data)
    passengers.save("passengers.txt")
    load_table()
def edit_passenger():
    row = int(win.lineEdit_row.text()) - 1
    col = int(win.lineEdit_col.text()) - 1
    new_value = win.lineEdit_new_value.text()
    if row < 0 or row >= win.tableWidget.rowCount():
        return
    if col < 0 or col >= win.tableWidget.columnCount():
        return
    old_data = [win.tableWidget.item(row, i).text() for i in range(4)]
    key = passengers.find_key(old_data)
    if key != -1:
        win.tableWidget.setItem(row, col, QTableWidgetItem(new_value))
        new_data = [win.tableWidget.item(row, i).text() for i in range(4)]
        passengers.edit(key, new_data)
        passengers.save("passengers.txt")
        load_table()
win.pushButton_load.clicked.connect(load_table)
win.pushButton_add.clicked.connect(add_passenger)
win.pushButton_edit.clicked.connect(edit_passenger)
win.pushButton_delete.clicked.connect(delete_passenger)
win.show()
sys.exit(app.exec())