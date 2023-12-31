import sys
import csv
import socket
from PySide6.QtCore import Slot, QThread, Signal, QCoreApplication, QRect
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QInputDialog, QLineEdit, QTableWidget, QWidget, QVBoxLayout, QListWidget, QFrame
from PySide6.QtGui import QTextCursor
from src import Ui_MainWindow, add_time, get_country_name, get_date, get_time

# Socket server thread
class ServerThread(QThread):
    # Define signals
    waiting_signal = Signal(str)
    connected_signal = Signal(str)
    received_msg = Signal(str)
    close_signal = Signal(str)
    reset_display_index = Signal(int)
    # Initialize server
    def __init__(self):
        super().__init__()
        host = socket.gethostbyname_ex(socket.gethostname())[2][0]
        port = 8080
        self.server = socket.socket()				
        self.server.bind((host, port))				
        self.server.listen(1)
        self.run_flag = True
    # Run server
    def run(self):
        while self.run_flag:
            self.waiting_signal.emit("Server: Waiting for client...")
            self.connection, address = self.server.accept()
            self.connected_signal.emit(f"Server: Connected to client {address}.")
            self.reset_display_index.emit(0)
            while True:
                msg = b''
                while True:
                    tmp = self.connection.recv(1024)
                    if not tmp:
                        break
                    msg += tmp
                    if msg == b'quit\n':
                        break
                    if msg.endswith(b"endOfMsg\n"):
                        break
                msg = msg.decode('utf-8')
                msg = msg.replace('endOfMsg\n', '')
                if msg == "quit\n":
                    break
                self.received_msg.emit(msg)
                send_msg = 'test'
                self.connection.sendall(bytes(f'{send_msg}\n', encoding='utf-8'))
            self.connection.close()
            self.close_signal.emit("Server: Connection closed!")
            self.reset_display_index.emit(-1)
    # Stop server
    def stop(self):
        self.terminate()
        self.wait()

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # Set console text
        self.console.setText('Console:')
        # Set layout
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        # Set splitter
        self.horizontalSplitter.setStretchFactor(0, 3)
        self.horizontalSplitter.setStretchFactor(1, 2)
        # Set tabWidget
        self.tabWidget.removeTab(1)
        self.tabWidget.removeTab(0)
        # Set tables and tabs list
        self.tables:list[QTableWidget] = []
        self.tabs:list[QWidget] = []
        self.display_index = -1
        # Naming sequence for new tabs
        self.history_tabs_number = 0
        # Store the data in current table before change
        self.table_data_storage = {
            'table_index' : -1,
            'table_data' : []
        }
        # Add the first table
        self.add_new_table()
        # Set property selector
        self.objectListWidget.setSelectionMode(QListWidget.MultiSelection)
        self.propertyComboBox.currentIndexChanged.connect(self.set_property_list_display)
        # Connect signals and slots of menubar
        self.actionSave.triggered.connect(self.save_table_to_csv)
        self.actionClear_table.triggered.connect(self.clear_tab)
        self.actionAdd_table.triggered.connect(self.add_new_table_forced)
        self.actionClear_table_content.triggered.connect(self.clear_table)
        self.actionSave_console.triggered.connect(self.save_console)
        # Connect signals and slots of objectListWidget
        self.objectListWidget.itemSelectionChanged.connect(self.set_table_by_property)
        # Begin server thread
        self.setup_server_thread()

    # Before closing window, ask if user want to quit and stop server thread
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.server_thread.stop()
            event.accept()
        else:
            event.ignore()
    # Start server thread
    def setup_server_thread(self):
        self.server_thread = ServerThread()
        self.server_thread.waiting_signal.connect(self.display_info_in_console)
        self.server_thread.connected_signal.connect(self.display_info_in_console)
        self.server_thread.connected_signal.connect(self.add_new_table)
        self.server_thread.received_msg.connect(self.display_msg_in_console)
        self.server_thread.received_msg.connect(self.display_msg_in_table)
        self.server_thread.received_msg.connect(self.set_property_filter)
        self.server_thread.close_signal.connect(self.display_info_in_console)
        self.server_thread.reset_display_index.connect(self.set_display_index)
        self.server_thread.start()
    # Display msg in textBrowser if msg has been changed
    @Slot(str)
    def display_msg_in_console(self, received_msg:str):
        self.console.moveCursor(QTextCursor.MoveOperation.End)  
        self.console.append(add_time("Client: "))
        self.console.insertPlainText(repr(received_msg))
    # Display information in textBrowser
    @Slot(str)
    def display_info_in_console(self, info:str):
        info = add_time(info) 
        self.console.append(info)
    # Save console to txt file
    @Slot()
    def save_console(self):
        # Get file name
        generated_name = f'{str(get_date())}-{str(get_time()).replace(":","")}-DCSExport'
        text, ok = QInputDialog.getText(self, "Save Console",
                                "Please enter file name:", QLineEdit.Normal,
                                generated_name)
        if ok and text:
            file_path = f'data/console_save/{text}.txt'
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.console.toPlainText())
    # Translate msg str to dict
    def msg_translate(self, msg:str)->dict:
        data = {}
        msg = msg.splitlines()
        for index, msg_line in enumerate(msg):
            # Tag line
            if index == 0:
                msg_line = msg_line.split(",")
                data['tag'] = msg_line
            else:
                msg_line = msg_line.split(",")
                data[index] = msg_line
        return data
    # Display msg in tableWidget
    @Slot(str)
    def display_msg_in_table(self, received_msg:str):
        table = self.tables[self.display_index]
        msg = self.msg_translate(received_msg)
        # Get all the column headers in table
        current_headers = []
        for index in range(table.columnCount()):
            current_headers.append(table.horizontalHeaderItem(index).text())
        # Set and renew headers
        for tag in msg['tag']:
            if tag not in current_headers:
                table.insertColumn(table.columnCount())
                tag = QTableWidgetItem(tag)
                table.setHorizontalHeaderItem(table.columnCount()-1, tag)
        # Add rows
        for index0 in range(1, len(msg)):
            table.insertRow(table.rowCount())
            # Link the specific data of each line to its tag
            object_data = {}
            for index1, tag in enumerate(msg['tag']):
                object_data[tag] = msg[index0][index1]
            # Link column tag to its column index
            tag_index = {}
            for index2 in range(table.columnCount()):
                tag_index[table.horizontalHeaderItem(index2).text()] = index2
            # Add data to the new row in the table
            for tag, data in object_data.items():
                column_index = tag_index[tag]
                if tag == 'country':
                    data = get_country_name(int(data))
                data = QTableWidgetItem(data)
                table.setItem(table.rowCount()-1, column_index, data)
        # Refresh table
        table.viewport().update()
    # Save table to csv file
    @Slot()
    def save_table_to_csv(self)->bool:
        table = self.tables[self.tabWidget.currentIndex()]
        # Get file name
        generated_name = f'{str(get_date())}-{str(get_time()).replace(":","")}-DCSExport'
        text, ok = QInputDialog.getText(self, "Save Table",
                                "Please enter file name:", QLineEdit.Normal,
                                generated_name)
        if ok and text:
            file_path = f'data/table_save/{text}.csv'
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                # Write headers
                headers = []
                for index in range(table.columnCount()):
                    headers.append(table.horizontalHeaderItem(index).text())
                writer.writerow(headers)
                # Write data
                for row in range(table.rowCount()):
                    row_data = []
                    for column in range(table.columnCount()):
                        item = table.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)
            return True
        else:
            return False
    # Clear table of the current tab
    @Slot()
    def clear_table(self):
        table = self.tables[self.tabWidget.currentIndex()]
        # Ask if user want to clear table
        reply = QMessageBox.question(self, 'Message', f"Do you want to save {self.tabWidget.tabText(self.tabWidget.currentIndex())}?", 
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save_table_to_csv()
        table.clear()
        table.setColumnCount(0)
        table.setRowCount(0)
        table.viewport().update()
    # Remove current tab
    @Slot()
    def clear_tab(self):
        # Ask if user want to clear table
        reply = QMessageBox.question(self, 'Message', f"Do you want to save {self.tabWidget.tabText(self.tabWidget.currentIndex())}?", 
                                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.save_table_to_csv()
        self.tabWidget.removeTab(self.tabWidget.currentIndex())
        self.tabs.pop(self.tabWidget.currentIndex())
        self.tables.pop(self.tabWidget.currentIndex())
    # Add new tab with table
    @Slot()
    def add_new_table(self):
        # Judge if current table is empty
        if self.tables:
            table = self.tables[self.tabWidget.currentIndex()]
            if table.rowCount() == 0:
                return
        self.history_tabs_number += 1
        self.tabs.append(QWidget())
        self.tables.append(QTableWidget(self.tabs[-1]))
        verticalLayout = QVBoxLayout(self.tabs[-1])
        verticalLayout.addWidget(self.tables[-1])
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.setSpacing(0)
        self.tables[-1].setFrameShape(QFrame.NoFrame)
        self.tables[-1].setFrameShadow(QFrame.Plain)
        self.tabWidget.addTab(self.tabs[-1], "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabs[-1]), f"Table {self.history_tabs_number}")
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tabs[-1]))
    # Add new tab with table without checking if current table is empty
    @Slot()
    def add_new_table_forced(self):
        self.history_tabs_number += 1
        self.tabs.append(QWidget())
        self.tables.append(QTableWidget(self.tabs[-1]))
        verticalLayout = QVBoxLayout(self.tabs[-1])
        verticalLayout.addWidget(self.tables[-1])
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        verticalLayout.setSpacing(0)
        self.tables[-1].setFrameShape(QFrame.NoFrame)
        self.tables[-1].setFrameShadow(QFrame.Plain)
        self.tabWidget.addTab(self.tabs[-1], "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabs[-1]), f"Table {self.history_tabs_number}")
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tabs[-1]))
    # Set the table that is going to display msg
    def set_display_index(self, index:int):
        if index == -1:
            self.display_index = -1
        else:
            self.display_index = self.tabWidget.currentIndex()
    # Get data from current table by tag
    def get_data_from_tag(self, tag:str)->list[str]:
        table = self.tables[self.tabWidget.currentIndex()]
        data = []
        column = -1
        for index in range(table.columnCount()):
            if table.horizontalHeaderItem(index).text() == tag:
                column = index
                break
        for row in range(table.rowCount()):
            item = table.item(row, column)
            if item is not None:
                data.append(item.text())
            else:
                data.append('')
        return data
    # Set property combobox items from headers of current table
    @Slot()
    def set_property_filter(self):
        table = self.tables[self.tabWidget.currentIndex()]
        # Get current items in combobox to a list
        current_items = []
        for index in range(self.propertyComboBox.count()):
            current_items.append(self.propertyComboBox.itemText(index))
        # Check all the column headers if they are already in comboBox. If not, add them
        for index in range(table.columnCount()):
            header = table.horizontalHeaderItem(index).text()
            if header not in current_items:
                self.propertyComboBox.addItem(header)
    # Set property list display
    @Slot(int)
    def set_property_list_display(self, index:int):
        data = self.get_data_from_tag(self.propertyComboBox.itemText(index))
        self.objectListWidget.clear()
        for item in data:
            # Judge if item is already in listWidget
            exist_flag = False
            for index in range(self.objectListWidget.count()):
                if self.objectListWidget.item(index).text() == item:
                    exist_flag = True
                    break
            if not exist_flag:
                self.objectListWidget.addItem(item)
    # Change the display of current table by selected objects
    @Slot()
    def set_table_by_property(self):
        if not self.propertyComboBox.currentText():
            # Restore the data of current table
            self.restore_table()
            return
        if self.objectListWidget.selectedItems() == []:
            self.restore_table()
            return
        # Read selected objects in objectListWidget
        selected_objects = self.objectListWidget.selectedItems()
        for index in range(len(selected_objects)):
            selected_objects[index] = selected_objects[index].text()
        # Store the data of current table
        current_table = self.tables[self.tabWidget.currentIndex()]
        current_table_data = []
        for row in range(current_table.rowCount()):
            row_data = {}
            for column in range(current_table.columnCount()):
                item = current_table.item(row, column)
                if item is not None:
                    row_data[current_table.horizontalHeaderItem(column).text()] = item.text()
                else:
                    row_data[current_table.horizontalHeaderItem(column).text()] = ''
            current_table_data.append(row_data)
        if self.table_data_storage['table_data'] == []:
            self.table_data_storage['table_data'] = current_table_data
            self.table_data_storage['table_index'] = self.tabWidget.currentIndex()
        # Set current table display according to selected objects
        table = self.tables[self.tabWidget.currentIndex()]
        # Clear table content
        table.clearContents()
        table.setRowCount(0)
        # Add data of selected objects
        for row in range(len(self.table_data_storage['table_data'])):
            if not self.table_data_storage['table_data'][row][self.propertyComboBox.currentText()] in selected_objects:
                continue
            table.insertRow(table.rowCount())
            for column in range(table.columnCount()):
                data = self.table_data_storage['table_data'][row][table.horizontalHeaderItem(column).text()]
                data = QTableWidgetItem(data)
                table.setItem(table.rowCount()-1, column, data)
        # Refresh table
        table.viewport().update()
    # Restore data to current table()
    def restore_table(self):
        # Restore the data of current table
        if self.table_data_storage['table_data']:
            table = self.tables[int(self.table_data_storage['table_index'])]
            table.clearContents()
            table.setRowCount(0)
            for row in range(len(self.table_data_storage['table_data'])):
                table.insertRow(table.rowCount())
                for column in range(table.columnCount()):
                    data = self.table_data_storage['table_data'][row][table.horizontalHeaderItem(column).text()]
                    data = QTableWidgetItem(data)
                    table.setItem(table.rowCount()-1, column, data)
            # Refresh table
            table.viewport().update()
            # Clear storage
            self.table_data_storage = {
                'table_index' : -1,
                'table_data' : []
            }


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()