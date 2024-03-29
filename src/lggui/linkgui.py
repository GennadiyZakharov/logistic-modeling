from __future__ import division
from PyQt4 import QtCore, QtGui
from lgcore.signals import signalUpdateGui, signalxChanged, signalyChanged, \
    signalFocusIn, signalEditLink
from lggui.packagegui import PackageGui
from math import sqrt


class LinkGui(QtGui.QGraphicsObject):
    '''
    This class containes all gui functionality for
    link between two nodes
    
    the position is treated as link beginning,
    the target is treated like line direction
    size and angle will be calculated according to this values
    '''
    arrowSize = 10
    arrowPoint1 = QtCore.QPointF(-arrowSize, arrowSize)
    arrowPoint2 = QtCore.QPointF(-arrowSize, -arrowSize) 
    
    def __init__(self, link, input, output, model, parent=None, scene=None, editMode=False):
        '''Input and output assumed to be nodegui type'''
        super(LinkGui, self).__init__(parent)
        self.link = link
        self.editMode = editMode
        self.model = model
        self.currentPlayer = model.players[model.currentPlayerIndex]
        self.connect(self.link, signalUpdateGui, self.onUpdateGui)
        
        self.paintOffset = 2 / 10
        
        self.input = input
        self.output = output
        
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | 
                      QtGui.QGraphicsItem.ItemIsFocusable)        
        self.gPackages = {}
      
        self.move()      
        
        self.connect(self.input, signalxChanged, self.move)
        self.connect(self.input, signalyChanged, self.move)
        self.connect(self.output, signalxChanged, self.move)
        self.connect(self.output, signalyChanged, self.move)
        self.onUpdateGui()
    
    def mouseDoubleClickEvent(self, event):
        self.update()
        if self.editMode :
            self.emit(signalEditLink,self)
        else :
            pass
        
    def move(self):
        self.position = self.input.center()
        self.setPos(self.position)
        self.direction = self.output.center() - self.position
        x, y = self.direction.x(), self.direction.y()
        self.length = sqrt(x * x + y * y)
        if self.length == 0 :
            return
        
        cosa, sina = x / self.length, y / self.length 
        matrix = QtGui.QTransform(cosa, sina, -sina, cosa, 0, 0)
        self.setTransform(matrix) 
        self.point2 = QtCore.QPointF(self.length, 0)

        for p in self.gPackages.keys():
            self.setPackageUpdateAge(self.gPackages[p], self.link.packages[p])
        self.update()
        
    def setPackageUpdateAge(self, gPackage, age):
        gPackage.setPos(self.point2 * (self.link.length - age) / self.link.length)
        
    def onUpdateGui(self):
        '''Repaint packages'''
        # Remove old packages and updated packages that already exist
        for p in self.gPackages.keys():
            if not self.link.packages.has_key(p):                
                self.gPackages[p].setParentItem(None)
                self.gPackages.pop(p)
            else :
                self.setPackageUpdateAge(self.gPackages[p], self.link.packages[p])
        # Add new packages
        for p in self.link.packages.keys():
            if not self.gPackages.has_key(p):
                self.gPackages[p] = PackageGui(p, self)
                self.setPackageUpdateAge(self.gPackages[p], self.link.packages[p])       
        if self.currentPlayer in self.link.viewers:
            toolTip = ('''<b>{0}</b>
                       <br />Length: {1}
                       <br />Cost: {2}
                       <br />Packages: {3}'''.format(self.link.name,
                                    self.link.length,self.link.cost,len(self.link.packages)))
        else:
            toolTip = 'You are not allowed <br />to see object properties'
        self.setToolTip(toolTip)
        self.update()
        
        
            
    def focusInEvent(self, event) :
        super(LinkGui, self).focusInEvent(event)
        self.emit(signalFocusIn, self)
    
    def setBrush(self, value) :
        self.brush = value
        
    def boundingRect(self):
        return QtCore.QRectF(QtCore.QPointF(0, -self.arrowSize), QtCore.QPointF(self.length, self.arrowSize))

    def shape(self):
        path = QtGui.QPainterPath()
        path.moveTo(QtCore.QPointF(0, 0))
        path.lineTo(self.point2)
        path.lineTo(self.point2 + self.arrowPoint1)
        path.moveTo(self.point2)
        path.lineTo(self.point2 + self.arrowPoint2)
        return path

    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtGui.QBrush(self.link.color), 5))
        painter.setBrush(QtGui.QBrush(self.link.color))
        painter.drawLine(QtCore.QPointF(0, 0), self.point2)
        painter.drawLine(self.point2, self.point2 + self.arrowPoint1)
        painter.drawLine(self.point2, self.point2 + self.arrowPoint2)
        painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(0,0,0)), 2))
        painter.drawText(self.boundingRect(),QtCore.Qt.AlignCenter,self.link.name)
        if self.hasFocus():
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(255,0,0)), 3))
            painter.drawEllipse(QtCore.QPointF(0, 0),3,3)
            painter.drawEllipse(self.point2,3,3)
