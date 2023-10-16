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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QScrollArea, QSizePolicy,
    QSplitter, QStatusBar, QTabWidget, QTextBrowser,
    QVBoxLayout, QWidget)

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
        self.actionSave_console = QAction(MainWindow)
        self.actionSave_console.setObjectName(u"actionSave_console")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSplitter = QSplitter(self.centralwidget)
        self.horizontalSplitter.setObjectName(u"horizontalSplitter")
        self.horizontalSplitter.setOrientation(Qt.Horizontal)
        self.tabWidget = QTabWidget(self.horizontalSplitter)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(10)
        self.tabWidget.setFont(font)
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalSplitter.addWidget(self.tabWidget)
        self.verticalSplitter = QSplitter(self.horizontalSplitter)
        self.verticalSplitter.setObjectName(u"verticalSplitter")
        self.verticalSplitter.setOrientation(Qt.Vertical)
        self.scrollArea = QScrollArea(self.verticalSplitter)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 502, 1000))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents.setMinimumSize(QSize(0, 1000))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.scrollAreaWidgetContents)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(10)
        font1.setItalic(True)
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label)

        self.propertyComboBox = QComboBox(self.scrollAreaWidgetContents)
        self.propertyComboBox.setObjectName(u"propertyComboBox")
        font2 = QFont()
        font2.setFamilies([u"Calibri"])
        font2.setItalic(True)
        self.propertyComboBox.setFont(font2)

        self.verticalLayout.addWidget(self.propertyComboBox)

        self.objectListWidget = QListWidget(self.scrollAreaWidgetContents)
        self.objectListWidget.setObjectName(u"objectListWidget")
        self.objectListWidget.setFont(font1)

        self.verticalLayout.addWidget(self.objectListWidget)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")

        self.verticalLayout.addWidget(self.groupBox)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalSplitter.addWidget(self.scrollArea)
        self.console = QTextBrowser(self.verticalSplitter)
        self.console.setObjectName(u"console")
        self.console.setFont(font2)
        self.verticalSplitter.addWidget(self.console)
        self.horizontalSplitter.addWidget(self.verticalSplitter)

        self.horizontalLayout.addWidget(self.horizontalSplitter)

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
        self.menuOptions.addAction(self.actionSave_console)
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
        self.actionSave_console.setText(QCoreApplication.translate("MainWindow", u"Save console", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Table 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Table 2", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select the property to filter:", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
    # retranslateUi

