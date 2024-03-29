from PyQt4 import QtCore, QtGui
from lgcore.signals import signalItemMoved, signalPackage

class DnDTableWidget(QtGui.QTableWidget):
    def __init__(self, parent=None):
        super(DnDTableWidget, self).__init__(parent)
        '''
        self.setRowCount(5)
        self.setColumnCount(3)
        #self.'''
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.dragEnabled()
        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.defaultDropAction = QtCore.Qt.MoveAction
        self.setDropIndicatorShown(True)
        self.dropAction = QtCore.Qt.MoveAction
        '''
        for i in range(self.rowCount()) :
            checkbox = QtGui.QCheckBox()
            self.setCellWidget(i,2,checkbox)
        '''
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text") and \
                                event.source().parent() is self.parent() :
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text") and \
                                event.source().parent() is self.parent() :
            row = self.rowAt(event.pos().y())
            col = self.columnAt(event.pos().x())
            if self.item(row, col) is None :
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()
            else :
                event.ignore()   
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text") and \
                                event.source().parent() is self.parent() :          
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            text = QtCore.QString()
            icon = QtGui.QIcon()
            stream >> text >> icon
            row = self.rowAt(event.pos().y())
            col = self.columnAt(event.pos().x())                
            item = QtGui.QTableWidgetItem(text, QtGui.QTableWidgetItem.Type)
            item.setIcon(icon)
            
            self.setItem(row, col, item)
            event.setDropAction(self.dropAction)
            self.emit(signalItemMoved, event.source(), self, col)
            event.accept()
        else:
            event.ignore()
    
    def startDrag(self, dropActions):
        item = self.currentItem()
        if item is None :
            return
        icon = item.icon()
        data = QtCore.QByteArray()
        col = self.column(item)
        stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
        stream << item.text() << icon
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/x-icon-and-text", data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        pixmap = icon.pixmap(24, 24)
        drag.setHotSpot(QtCore.QPoint(12, 12))
        drag.setPixmap(pixmap)
        if (drag.start(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction):
            
            packageItem = self.takeItem(self.row(item), col)
            self.emit(signalPackage, packageItem.package, col)
