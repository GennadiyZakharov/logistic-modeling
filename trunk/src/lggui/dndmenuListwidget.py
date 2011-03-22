from PyQt4 import QtCore, QtGui

class DnDMenuListWidget(QtGui.QListWidget):
    def __init__(self, parent=None):
        super(DnDMenuListWidget, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.dropAction = QtCore.Qt.MoveAction
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text") and \
                                event.source().parent() is self.parent() :
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text") and \
                                event.source().parent() is self.parent() : 
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-icon-and-text")  and \
                                event.source().parent() is self.parent() :
            data = event.mimeData().data("application/x-icon-and-text")
            stream = QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            text = QtCore.QString()
            icon = QtGui.QIcon()
            stream >> text >> icon
            self.dropAction = QtCore.Qt.MoveAction

            item = QtGui.QListWidgetItem(text, self)
            item.setIcon(icon)
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
        if (drag.start(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction):
            self.takeItem(self.row(item))

        
