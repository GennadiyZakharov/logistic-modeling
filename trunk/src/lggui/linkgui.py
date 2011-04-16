from __future__ import division
from math import sqrt

from PyQt4 import QtCore, QtGui
from lgcore.signals import signalUpdateGui, signalxChanged, signalyChanged
from lggui.packagegui import PackageGui

class LinkGui(QtGui.QGraphicsObject):
    '''
    This class containes all gui functionality for
    link between two nodes
    
    the position is treated as link beginning,
    the target is treated like line direction
    size and angle will be calculated according to this values
    '''
    arrowSize = 5
    arrowPoint1 = QtCore.QPointF(-arrowSize,arrowSize)
    arrowPoint2 = QtCore.QPointF(-arrowSize,-arrowSize) 
    
    def __init__(self, link, input, output, parent=None, scene=None):
        '''Input and output assumed to be nodegui type'''
        super(LinkGui, self).__init__(parent)
        self.link = link
        self.connect(self.link, signalUpdateGui, self.on_updateGui)
        
        self.paintOffset = 2 / 10
        
        self.input = input
        self.output = output
        
        self.color = QtGui.QColor(0, 0, 0)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | 
                      QtGui.QGraphicsItem.ItemIsFocusable)        
        self.gPackages = {}
      
        self.move()      
        
        self.connect(self.input, signalxChanged, self.move)
        self.connect(self.input, signalyChanged, self.move)
        self.connect(self.output, signalxChanged, self.move)
        self.connect(self.output, signalyChanged, self.move)
        
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
        print self.link.length - age
        gPackage.setPos(self.point2 * (self.link.length - age) / self.link.length)
        
    def on_updateGui(self):
        '''Repaint packages'''
        # Remove old packages and updated packages that already exist
        for p in self.gPackages.keys():
            if not self.link.packages.has_key(p):                
                self.gPackages[p].setParentItem(None)
                self.gPackages.pop(p) # TODO: Check correctness
            else :
                self.setPackageUpdateAge(self.gPackages[p], self.link.packages[p])
        # Add new packages
        for p in self.link.packages.keys():
            if not self.gPackages.has_key(p):
                self.gPackages[p] = PackageGui(p, self)
                self.setPackageUpdateAge(self.gPackages[p], self.link.packages[p])
            
         
    def mouseDoubleClickEvent(self, event):
        #dialog = TextItemDlg(self, self.parentWidget())
        #dialog.exec_()
        #self.rotate(180)
        self.update()
    
    def setBrush(self, value) :
        self.brush = value
        
    def boundingRect(self):
        return QtCore.QRectF(QtCore.QPointF(0, -self.arrowSize), QtCore.QPointF(self.length, self.arrowSize))

    def shape(self):
        path = QtGui.QPainterPath()
        path.moveTo(QtCore.QPointF(0, 0))
        path.lineTo(self.point2)
        path.lineTo(self.point2+self.arrowPoint1)
        path.moveTo(self.point2)
        path.lineTo(self.point2+self.arrowPoint2)
        return path

    def paint(self, painter, option, widget=None):
        painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(205, 235, 139)), 2.5))
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawLine(QtCore.QPointF(0, 0), self.point2)
        painter.drawLine(self.point2,self.point2+self.arrowPoint1)
        painter.drawLine(self.point2,self.point2+self.arrowPoint2)