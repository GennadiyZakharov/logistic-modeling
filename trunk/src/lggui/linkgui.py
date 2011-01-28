'''
Created on 26.01.2011

@author: gena
'''

'''
Created on 25.01.2011

@author: gena
'''

from PyQt4 import QtCore,QtGui
#from ltcore.actions import LtActions
from lgcore.signals import *

class LinkGui(QtGui.QGraphicsItem):
    '''
    This class containes all gui functionality for
    link between two nodes
    
    the position is treated as link beginning,
    the target is treated like line direction
    size and angle will be calculated according to this values
    
    '''
    
    def __init__(self,position,target,parent=None):
        super(LinkGui, self).__init__()
        self.color = QtGui.QColor(0, 255, 0)
        self.parent = parent
        self.move(position,target)
        #self.brush = QtCore.Qt.NoPen
        self.acceptDrops()
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable|
        QtGui.QGraphicsItem.ItemIsMovable|QtGui.QGraphicsItem.ItemIsFocusable)
        
        self.setFocus()
        
    def move(self,position=None,target=None):
        if position :
            self.setPos(position)
        if target is not None :
            self.direction = target - position
        self.update()
        
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
        return QtCore.QRectF(QtCore.QPointF(0,0),self.direction)

    def shape(self):
        path = QtGui.QPainterPath()
        path.moveTo(QtCore.QPointF(0,0))
        path.lineTo(self.direction)
        path.addEllipse(self.direction,3,3)
        return path


    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,255)), 2.5))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawLine(QtCore.QPointF(0,0),self.direction)
        painter.drawEllipse(self.direction,3,3)

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