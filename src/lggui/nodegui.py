'''
Created on 25.01.2011

@author: gena
'''

from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *

class NodeGui(QtGui.QGraphicsItem):
    '''
    This class containes all gui functionality for
    node
    '''
    Rect = QtCore.QRectF(-30, -20, 60, 40)
    
    def __init__(self,position,parent=None):
        super(NodeGui, self).__init__()
        self.color = 0
        self.parent = parent
        self.setPos(position)
        self.brush = QtCore.Qt.NoPen
        self.acceptDrops()
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable|
        QtGui.QGraphicsItem.ItemIsMovable|QtGui.QGraphicsItem.ItemIsFocusable)
        
        self.setFocus()
        
    def mouseDoubleClickEvent(self, event):
        #dialog = TextItemDlg(self, self.parentWidget())
        #dialog.exec_()
        self.rotate(180)
        self.update()
    
    def setBrush(self,value) :
        self.brush = value
        
    def keyPressEvent(self, event):
        factor = 8
        x = self.x()
        y = self.y()
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            if event.key() == QtCore.Qt.Key_Left:
                x-= factor
            elif event.key() == QtCore.Qt.Key_Right:
                x+= factor
            elif event.key() == QtCore.Qt.Key_Up:
                y-= factor
            elif event.key() == QtCore.Qt.Key_Down:
                y+= factor
            self.setPos(QtCore.QPointF(x, y))
            self.update()
        else:
            QtGui.QGraphicsItem.keyPressEvent(self, event)


    def boundingRect(self):
        return self.Rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.Rect)
        return path


    def paint(self, painter, option, widget=None):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawEllipse(self.Rect)

'''
    def contextMenuEvent(self, event):
    wrapped = []
    menu = QMenu(self.parent)
    for text, param in (
          ("&Solid", Qt.SolidLine),
          ("&Dashed", Qt.DashLine),
          ("D&otted", Qt.DotLine),
          ("D&ashDotted", Qt.DashDotLine),
          ("DashDo&tDotted", Qt.DashDotDotLine)):
        wrapper = functools.partial(self.setBrush, param)
        wrapped.append(wrapper)
        menu.addAction(text, wrapper)
    menu.exec_(event.screenPos())
'''