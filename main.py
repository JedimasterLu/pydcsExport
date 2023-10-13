import sys
import socket
from PySide6.QtCore import Slot, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtGui import QTextCursor
from src import Ui_MainWindow, add_time, get_country_name

# Socket server thread
class ServerThread(QThread):
    # Define signals
    waiting_signal = Signal(str)
    connected_signal = Signal(str)
    received_msg = Signal(str)
    close_signal = Signal(str)
    # Initialize server
    def __init__(self):
        super().__init__()
        host = '2.0.0.1'
        port = 8000
        self.server = socket.socket()				
        self.server.bind((host, port))				
        self.server.listen(1)
    # Run server
    def run(self):
        while True:
            self.waiting_signal.emit("Server: Waiting for client...")
            self.connection, address = self.server.accept()
            self.connected_signal.emit(f"Server: Connected to client {address}.")
            while True:
                msg = self.connection.recv(1024)
                msg = msg.decode('utf-8')
                if msg == "quit":
                    break
                self.received_msg.emit(msg)
                send_msg = 'test'
                self.connection.send(bytes(f'{send_msg}\n', encoding='utf-8'))
            self.connection.close()
            self.close_signal.emit("Server: Connection closed!")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.console.setText('Console:')
        
        self.setup_server_thread()

        self.last_msg = ''
        self.msg = ''

    def setup_server_thread(self):
        self.server_thread = ServerThread()
        self.server_thread.waiting_signal.connect(self.display_info_in_console)
        self.server_thread.connected_signal.connect(self.display_info_in_console)
        self.server_thread.received_msg.connect(self.display_msg_in_console)
        self.server_thread.received_msg.connect(self.display_msg_in_table)
        self.server_thread.close_signal.connect(self.display_info_in_console)
        self.server_thread.close_signal.connect(self.clear_msgs)
        self.server_thread.start()

    # Display msg in textBrowser if msg has been changed
    @Slot(str)
    def display_msg_in_console(self, received_msg:str):
        self.msg = received_msg
        if self.last_msg != self.msg:
            self.last_msg = self.msg
            self.console.moveCursor(QTextCursor.MoveOperation.End)  
            self.console.append(add_time("Client: "))
            self.console.insertPlainText(repr(self.msg))
    # Display information in textBrowser
    @Slot(str)
    def display_info_in_console(self, info:str):
        info = add_time(info) 
        self.console.append(info)
    # Clear stored msgs
    @Slot()
    def clear_msgs(self):
        self.last_msg = ''
        self.msg = ''
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
        msg = self.msg_translate(received_msg)
        # Get all the column headers in table
        current_headers = []
        for index in range(self.table.columnCount()):
            current_headers.append(self.table.horizontalHeaderItem(index).text())
        # Set and renew headers
        for tag in msg['tag']:
            if tag not in current_headers:
                self.table.insertColumn(self.table.columnCount())
                tag = QTableWidgetItem(tag)
                self.table.setHorizontalHeaderItem(self.table.columnCount()-1, tag)
        # Add rows
        for index0 in range(1, len(msg)):
            self.table.insertRow(self.table.rowCount())
            # Link the specific data of each line to its tag
            object_data = {}
            for index1, tag in enumerate(msg['tag']):
                object_data[tag] = msg[index0][index1]
            print(object_data)
            # Link column tag to its column index
            tag_index = {}
            for index2 in range(self.table.columnCount()):
                tag_index[self.table.horizontalHeaderItem(index2).text()] = index2
            print(tag_index)
            # Add data to the new row in the table
            for tag, data in object_data.items():
                column_index = tag_index[tag]
                data = QTableWidgetItem(data)
                self.table.setItem(self.table.rowCount()-1, column_index, data)
        # Refresh table
        self.table.viewport().update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()