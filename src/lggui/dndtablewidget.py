'''
Created on 10.03.2011

@author: Gena
'''
from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *

class DnDTableWidget(QtGui.QTableWidget):
    '''
    classdocs
    '''


    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(DnDTableWidget, self).__init__(parent)
        self.setRowCount(5)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["Column #1", "Column #2"])

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.dragEnabled()
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDropIndicatorShown(True)
        self.dropAction = QtCore.Qt.MoveAction
        
        for i in range(self.rowCount()) :
            checkbox = QtGui.QCheckBox()
            self.setCellWidget(i,2,checkbox)
        
        item = QtGui.QTableWidgetItem('testitem', QtGui.QTableWidgetItem.UserType)
        item.setIcon(QtGui.QIcon('E:\usb.png'))
        
        self.setItem(0,0,item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    
    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text"):
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            text = QtCore.QString()
            icon = QtGui.QIcon()
            stream >> text >> icon

            item = QtGui.QTableWidgetItem(text, QtGui.QTableWidgetItem.Type)
            item.setIcon(icon)
            print('accept')
            self.setItem(1,2,item)
            event.setDropAction(self.dropAction)
            event.accept()            
        else:
            event.ignore()
    
    def startDrag(self, dropActions):
        item = self.currentItem()
        icon = item.icon()
        data = QtCore.QByteArray()
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream << item.text() << icon
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QtCore.QPoint(12, 12))
        drag.setPixmap(pixmap)
        if (drag.start(QtCore.Qt.MoveAction|QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction):
            self.takeItem(self.row(item),self.column(item))
