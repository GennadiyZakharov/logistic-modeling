from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from PyQt4.QtCore import QString
from PyQt4.QtGui import (QBoxLayout,
        QLabel, QLineEdit, QTextEdit,
        QWidget)

LEFT, ABOVE = range(2)

class LabelledLineEdit(QWidget):

    def __init__(self, labelText=QString(), position=LEFT,
                 parent=None):
        super(LabelledLineEdit, self).__init__(parent)
        self.label = QLabel(labelText)
        self.lineEdit = QLineEdit()
        self.label.setBuddy(self.lineEdit)
        layout = QBoxLayout(QBoxLayout.LeftToRight
                if position == LEFT else QBoxLayout.TopToBottom)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)
        self.setLayout(layout)

class LabelledTextEdit(QWidget):

    def __init__(self, labelText=QString(), position=LEFT,
                 parent=None):
        super(LabelledTextEdit, self).__init__(parent)
        self.label = QLabel(labelText)
        self.textEdit = QTextEdit()
        self.label.setBuddy(self.textEdit)
        layout = QBoxLayout(QBoxLayout.LeftToRight
                if position == LEFT else QBoxLayout.TopToBottom)
        layout.addWidget(self.label)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
