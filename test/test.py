# -*- coding: utf-8 -*-

import time


from PySide6.QtCore import (QThread, Signal, Slot, QSize)
from PySide6.QtWidgets import (QApplication, QPushButton, QLabel, QVBoxLayout, QWidget)


class MyThread(QThread):
    my_signal = Signal(int)
    finished_signal = Signal()

    def __init__(self, count):
        super().__init__()
        self.count: int = count

    def run(self):
        for idx in range(1, self.count + 1):
            time.sleep(1)
            # 任务进行时发出信号
            self.my_signal.emit(idx)
	    # 任务完成后发出信号
        self.finished_signal.emit()


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setup_ui()
        #
        self.button.clicked.connect(self.setup_thread)

    def setup_ui(self):
        self.setWindowTitle('demo')
        self.resize(QSize(250, 180))
        # 创建一个垂直布局
        layout = QVBoxLayout()
        # 创建一个标签
        self.label = QLabel('This is a label => ')
        layout.addWidget(self.label)
        # 创建一个按钮
        self.button = QPushButton('Send Request')
        layout.addWidget(self.button)
        # 将布局设置为主窗口的布局
        self.setLayout(layout)
        # 显示窗口
        self.show()

    def setup_thread(self):
        self.thread_ = MyThread(count=5)
        self.thread_.my_signal.connect(self.thread_progress)
        self.thread_.finished_signal.connect(self.thread_finished)
        self.thread_.start()

    @Slot(int)
    def thread_progress(self, item):
        self.label.setText('This is a label => ' + str(item))

    @Slot()
    def thread_finished(self):
        self.label.setText('This is a label finished.')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
