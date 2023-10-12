import sys
import socket
from PySide6 import QtGui
from PySide6.QtCore import Slot, QTimer, QThread, Signal
from PySide6.QtWidgets import QApplication, QMainWindow
from src.ui.DCSExport_ui import Ui_MainWindow

class ServerThread(QThread):

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
            self.connection, address = self.server.accept()
            self.connected_signal.emit("Server connected!")
            while True:
                msg = self.connection.recv(1024)
                msg = msg.decode('utf-8')
                if msg == "Quit\n":
                    break
                self.received_msg.emit(msg)
                send_msg = 'test'
                send_msg = send_msg.encode(encoding='utf-8', errors='strict')
                self.connection.send(send_msg)
            self.server.close()
            self.close_signal.emit("Server closed!")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.console.setText('Console:\n')
        
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
            self.console.setText(received_msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainW = MainWindow()
    ui = Ui_MainWindow()  
    ui.setupUi(MainW)
    MainW.show()
    app.exec()