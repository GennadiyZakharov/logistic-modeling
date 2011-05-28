#!/usr/bin/env python

import sys
from os.path import join, abspath, pardir
from PyQt4.QtGui import QApplication, QIcon

sys.path.append(abspath(join(pardir, 'src')))
sys.path.append(abspath(join(pardir, 'resources')))
from lggui.playermainwindow import PlayerMainWindow

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("Org")
    app.setOrganizationDomain(".ru")
    app.setApplicationName("Logistic-modeling")
    app.setWindowIcon(QIcon(":/icon.png"))
    mainWindow = PlayerMainWindow()
    mainWindow.show()
    return app.exec_()

if __name__ == '__main__':
    main()