# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DCSExport.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QTabWidget, QTextBrowser,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionClear_table = QAction(MainWindow)
        self.actionClear_table.setObjectName(u"actionClear_table")
        self.actionAdd_table = QAction(MainWindow)
        self.actionAdd_table.setObjectName(u"actionAdd_table")
        self.actionClear_tab = QAction(MainWindow)
        self.actionClear_tab.setObjectName(u"actionClear_tab")
        self.actionClear_table_content = QAction(MainWindow)
        self.actionClear_table_content.setObjectName(u"actionClear_table_content")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.console = QTextBrowser(self.centralwidget)
        self.console.setObjectName(u"console")
        self.console.setGeometry(QRect(440, 0, 361, 561))
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setItalic(True)
        self.console.setFont(font)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 441, 561))
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 800, 22))
        self.menuOptions = QMenu(self.menuBar)
        self.menuOptions.setObjectName(u"menuOptions")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuOptions.menuAction())
        self.menuOptions.addAction(self.actionSave)
        self.menuOptions.addAction(self.actionAdd_table)
        self.menuOptions.addAction(self.actionClear_table)
        self.menuOptions.addAction(self.actionClear_table_content)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(statustip)
        self.actionSave.setStatusTip(QCoreApplication.translate("MainWindow", u"Save current table to .csv file", None))
#endif // QT_CONFIG(statustip)
        self.actionClear_table.setText(QCoreApplication.translate("MainWindow", u"Clear table", None))
#if QT_CONFIG(statustip)
        self.actionClear_table.setStatusTip(QCoreApplication.translate("MainWindow", u"Clear current table", None))
#endif // QT_CONFIG(statustip)
        self.actionAdd_table.setText(QCoreApplication.translate("MainWindow", u"Add table", None))
        self.actionClear_tab.setText(QCoreApplication.translate("MainWindow", u"Clear tab", None))
        self.actionClear_table_content.setText(QCoreApplication.translate("MainWindow", u"Clear table content", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Table 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Table 2", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

