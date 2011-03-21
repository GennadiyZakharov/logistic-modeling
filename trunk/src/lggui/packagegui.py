'''
Created on 21.03.2011

@author: Gena
'''
from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *

class PackageGui(QtGui.QGraphicsObject):
    '''
    This class paint package
    '''
    
    def __init__(self,package,parent=None):
        '''
        Draw package
        '''
        super(PackageGui, self).__init__(parent)
        self.package = package
        #self.connect(self.package, signalUpdateGui, self.on_updateGui)
        
        self.color = QtGui.QColor(100, 255, 50)
        self.rect = QtCore.QRectF(-15,-15,30,30)
        
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable|
                      QtGui.QGraphicsItem.ItemIsFocusable)
          
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
        painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,255)), 1.5))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(self.rect)
