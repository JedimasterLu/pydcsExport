import sys
import socket
from PySide6.QtCore import Slot, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow
from src import Ui_MainWindow, add_time, get_country_name

class ServerThread(QThread):

    waiting_signal = Signal(str)
    connected_signal = Signal(str)
    received_msg = Signal(str)
    close_signal = Signal(str)

    def __init__(self):
        super().__init__()
        host = '2.0.0.1'
        port = 8000
        self.server = socket.socket()				
        self.server.bind((host, port))				
        self.server.listen(1)

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
                msg = add_time(msg)
                self.received_msg.emit(f'  Client: {msg}')
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
        self.server_thread.connected_signal.connect(self.display_msg)
        self.server_thread.received_msg.connect(self.display_msg)
        self.server_thread.close_signal.connect(self.display_msg)
        self.server_thread.start()

    # Display msg in textBrowser if msg has been changed
    @Slot(str)
    def display_msg(self, received_msg):
        self.msg = received_msg
        if self.last_msg != self.msg:
            self.last_msg = self.msg
            self.console.append(received_msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()