from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import sys
import os

class Passenger:
    def __init__(self, name='', flight='', seat_class='', baggage=''):
        self.name = name
        self.flight = flight
        self.seat_class = seat_class
        self.baggage = baggage
        
    def to_list(self): 
        return [self.name, self.flight, self.seat_class, self.baggage]
    
    def equals(self, other):
        return self.to_list() == other.to_list()

class PassengerManager:
    def __init__(self): 
        self.passengers = {}
        self.count = 0
        
    def add_passenger(self, passenger): 
        self.passengers[self.count] = passenger
        self.count += 1
        
    def delete_passenger(self, index):
        if index in self.passengers:
            del self.passengers[index]
            
    def edit_passenger(self, index, col, value):
        if index in self.passengers:
            attrs = self.passengers[index].to_list()
            attrs[col] = value
            self.passengers[index] = Passenger(*attrs)
    
    def find_key(self, data):
        target = Passenger(*data)
        for key, passenger in self.passengers.items():
            if passenger.equals(target):
                return key
        return -1
            
    def load_from_file(self, filename="passengers.txt"):
        self.passengers = {}
        self.count = 0
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            if ';' in line:
                                data = [part.strip() for part in line.split(';')]
                            else:
                                data = [part.strip() for part in line.split(',')]
                            if len(data) == 4:
                                self.add_passenger(Passenger(*data))
            else:
                with open(filename, 'w', encoding='utf-8') as f:
                    pass
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"Ошибка загрузки данных:\n{str(e)}")
            
    def save_to_file(self, filename="passengers.txt"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for p in self.passengers.values():
                    f.write(';'.join(p.to_list()) + '\n')
            return True
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"Ошибка сохранения данных:\n{str(e)}")
            return False

class AddPassengerDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("add_passenger.ui", self)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 12px;
            }
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.parent = parent
        self.addBtn.clicked.connect(self.add_passenger)
        
    def add_passenger(self):
        data = [
            self.nameEdit.text().strip(),
            self.flightEdit.text().strip(),
            self.classEdit.text().strip(),
            self.baggageEdit.text().strip()
        ]
        if all(data):
            self.parent.passenger_manager.add_passenger(Passenger(*data))
            if self.parent.passenger_manager.save_to_file():
                self.parent.update_table()
                self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")

class EditPassengerDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("edit_passenger.ui", self)
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 12px;
            }
            QLineEdit, QComboBox {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.parent = parent
        self.editBtn.clicked.connect(self.edit_passenger)
        
    def edit_passenger(self):
        try:
            row = int(self.rowEdit.text())
            col = self.columnCombo.currentIndex()
            value = self.valueEdit.text().strip()
            
            if row in self.parent.passenger_manager.passengers and value:
                self.parent.passenger_manager.edit_passenger(row, col, value)
                if self.parent.passenger_manager.save_to_file():
                    self.parent.update_table()
                    self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Некорректные данные!")
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите корректный номер строки!")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Установка иконки приложения
        self.setWindowIcon(QIcon('app_icon.png'))  # Убедитесь, что файл app_icon.png существует
        
        uic.loadUi("passenger_ui.ui", self)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #34495e;
            }
            QTableWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                gridline-color: #7f8c8d;
                font-size: 12px;
                selection-background-color: #3498db;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        
        self.passenger_manager = PassengerManager()
        self.passenger_manager.load_from_file()
        
        self.passengersTable.setColumnCount(4)
        self.passengersTable.setHorizontalHeaderLabels(["ФИО", "Рейс", "Класс", "Вес багажа"])
        self.passengersTable.horizontalHeader().setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.passengersTable.verticalHeader().setVisible(False)
        self.passengersTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        self.addBtn.clicked.connect(lambda: AddPassengerDialog(self).exec_())
        self.editBtn.clicked.connect(lambda: EditPassengerDialog(self).exec_())
        self.deleteBtn.clicked.connect(self.delete_selected)
        self.loadBtn.clicked.connect(self.load_data)
        
        self.update_table()
        
    def update_table(self):
        self.passengersTable.setRowCount(len(self.passenger_manager.passengers))
        for row, (key, passenger) in enumerate(self.passenger_manager.passengers.items()):
            for col, value in enumerate(passenger.to_list()):
                item = QtWidgets.QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.passengersTable.setItem(row, col, item)
        
        for i, width in enumerate([250, 100, 80, 100]):
            self.passengersTable.setColumnWidth(i, width)
            
    def load_data(self):
        self.passenger_manager.load_from_file()
        self.update_table()
        QtWidgets.QMessageBox.information(self, "Успех", "Данные успешно загружены из passengers.txt")
        
    def delete_selected(self):
        selected_row = self.passengersTable.currentRow()
        if selected_row >= 0:
            reply = QtWidgets.QMessageBox.question(
                self, 'Подтверждение', 
                'Вы уверены, что хотите удалить этого пассажира?',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                row_data = []
                for col in range(4):
                    item = self.passengersTable.item(selected_row, col)
                    if item:
                        row_data.append(item.text())
                
                key = self.passenger_manager.find_key(row_data)
                if key != -1:
                    self.passenger_manager.delete_passenger(key)
                    if self.passenger_manager.save_to_file():
                        self.update_table()
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Выберите пассажира для удаления!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Установка иконки для всего приложения (для Windows)
    app.setWindowIcon(QIcon('app_icon.png'))
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())