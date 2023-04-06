# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/app_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AppWindow(object):
    def setupUi(self, AppWindow):
        AppWindow.setObjectName("AppWindow")
        AppWindow.resize(1183, 841)
        self.centralwidget = QtWidgets.QWidget(AppWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_init = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_init.setFont(font)
        self.label_init.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_init.setAlignment(QtCore.Qt.AlignCenter)
        self.label_init.setObjectName("label_init")
        self.verticalLayout.addWidget(self.label_init)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        AppWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AppWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1183, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        AppWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AppWindow)
        self.statusbar.setObjectName("statusbar")
        AppWindow.setStatusBar(self.statusbar)
        self.actionAbout = QtWidgets.QAction(AppWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionShow_Debugging_Window = QtWidgets.QAction(AppWindow)
        self.actionShow_Debugging_Window.setCheckable(True)
        self.actionShow_Debugging_Window.setObjectName("actionShow_Debugging_Window")
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionShow_Debugging_Window)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(AppWindow)
        QtCore.QMetaObject.connectSlotsByName(AppWindow)

    def retranslateUi(self, AppWindow):
        _translate = QtCore.QCoreApplication.translate
        AppWindow.setWindowTitle(_translate("AppWindow", "MainWindow"))
        self.label_init.setText(_translate("AppWindow", "Initializing, can take few seconds when running first time"))
        self.menuHelp.setTitle(_translate("AppWindow", "Help"))
        self.actionAbout.setText(_translate("AppWindow", "About"))
        self.actionShow_Debugging_Window.setText(_translate("AppWindow", "Show Debugging Window"))
