#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 

@author: gena
'''
import sys

#125/75

from PyQt4.QtGui import QApplication,QIcon
from os.path import join, abspath, pardir

sys.path.append(abspath(join(pardir, 'src')))
sys.path.append(abspath(join(pardir, 'resources')))

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
    