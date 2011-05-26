from PyQt4 import QtCore, QtGui

class PackageGui(QtGui.QGraphicsObject):
    '''This class paint package'''
    
    def __init__(self, package, parent=None):
        super(PackageGui, self).__init__(parent)
        self.package = package
        #self.connect(self.package, signalUpdateGui, self.on_updateGui)
        
        self.rect = QtCore.QRectF(-15, -15, 30, 30)
        
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | 
                      QtGui.QGraphicsItem.ItemIsFocusable)
        
        #self.hashValue = int(sha512(str(time())).hexdigest(), 16) 


    #def __hash__(self):
    #    return self.hashValue
    
    #def __str__(self):
    #    return 'gPackage' + str(self.hashValue)
    
    def mouseDoubleClickEvent(self, event):
        #dialog = TextItemDlg(self)
        #dialog.exec_()
        self.update()
        
    def on_updateGui(self):
        pass
    
    def boundingRect(self):
        return self.rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.rect)
        return path

    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(205, 235, 139)), 1.5))
        painter.setBrush(QtGui.QBrush(self.package.color))
        painter.drawEllipse(self.rect)
