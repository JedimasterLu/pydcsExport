import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from src import DCSExport_ui

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = DCSExport_ui.Ui_MainWindow()  
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec()
