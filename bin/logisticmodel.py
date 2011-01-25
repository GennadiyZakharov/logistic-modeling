#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 

@author: gena
'''
import sys

from PyQt4.QtGui import QApplication,QIcon

#print(sys.path) TODO: append sys path

# sys.path.append("../ltcore")
# sys.path.append("../ltgui")
# print(sys.path)

from lggui.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Org")
    app.setOrganizationDomain(".ru")
    app.setApplicationName("Logistic-modeling")
    app.setWindowIcon(QIcon(":/icon.png"))
    mainWindow = MainWindow()
    mainWindow.show()
    return app.exec_()

if __name__ == '__main__':
    main()
    