
# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QWidget, QTableWidget,
                               QTableWidgetItem, QVBoxLayout)
 
colors = [("Red", "#FF0000"),
          ("Green", "#00FF00"),
          ("Blue", "#0000FF"),
          ("Black", "#000000"),
          ("White", "#FFFFFF"),
          ("Electric Green", "#41CD52"),
          ("Dark Blue", "#222840"),
          ("Yellow", "#F9E56d")]
 
 
def get_rgb_from_hex(code):
    code_hex = code.replace("#", "")
    rgb = tuple(int(code_hex[i:i+2], 16) for i in (0, 2, 4))
    return QColor.fromRgb(rgb[0], rgb[1], rgb[2])
 
 
class tableData(QWidget):
    def __init__(self, parent=None):
        super(tableData, self).__init__(parent)
        self.setWindowTitle("My TableData")
 
        self.table = QTableWidget()
        self.table.setRowCount(len(colors))
        self.table.setColumnCount(len(colors[0]) + 1)
        self.table.setHorizontalHeaderLabels(["Name", "Hex Code", "Color"])
 
        for i, (name, code) in enumerate(colors):
            item_name = QTableWidgetItem(name)
            item_code = QTableWidgetItem(code)
            item_color = QTableWidgetItem()
            item_color.setBackground(get_rgb_from_hex(code))
            self.table.setItem(i, 0, item_name)
            self.table.setItem(i, 1, item_code)
            self.table.setItem(i, 2, item_color)
 
        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

        header0 = self.table.horizontalHeaderItem(1)
        print(header0.text())
        idx = self.table.indexFromItem(header0)
        print(idx.data())
 
 
if __name__ == "__main__":
    app = QApplication([])
    window = tableData()
    window.show()
    sys.exit(app.exec())