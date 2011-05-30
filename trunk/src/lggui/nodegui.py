from __future__ import division
from PyQt4 import QtCore, QtGui
from lgcore.signals import signalUpdateGui, signalClicked, signalExecuteDialog, \
    signalFocusIn, signalItemMoved
from lggui.nodewidget import NodeWidget

class NodeGui(QtGui.QGraphicsObject):
    '''This class containes all gui functionality for node'''
    Rect = QtCore.QRectF(0, 0, 120, 150)
    NameRect = QtCore.QRectF(0,0,Rect.width(),40)
    InfoRect = QtCore.QRectF(0,50,Rect.width(),100)
    
    def __init__(self, node, parent=None, scene=None):
        
        super(NodeGui, self).__init__(parent)
        #QtCore.QObject.__init__(self) 
        
        self.node = node
        self.connect(self.node, signalUpdateGui, self.onUpdateGui)
        #self.connect(self.node, signalExecuteDialog, self.onExecuteDialog)

        self.xChanged.connect(self.onMove)
        self.yChanged.connect(self.onMove)
        self.setPos(node.pos)
        
        self.acceptDrops()
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | 
        QtGui.QGraphicsItem.ItemIsMovable | QtGui.QGraphicsItem.ItemIsFocusable)
        
        self.links = []
               
        self.mainwidget = NodeWidget(self.node, None)
        '''
        self.proxy = QtGui.QGraphicsProxyWidget(self)
        self.proxy.setWidget(self.mainwidget)
        self.proxy.setPos(QtCore.QPointF(0, 30))
        '''
        
    def onMove(self):
        self.emit(signalItemMoved,self.pos()) 
        
    def center(self):
        rect = QtCore.QRectF(self.Rect)
        rect.moveTo(self.pos())
        return rect.center()
    
    def addLink(self, link):
        self.links.append(link)
        #QtCore.QObject.connect(self, signalNodeMoved,link.on_NodeMoved)
    ''' 
    def dropEvent(self, event):
        print "Drop"
        for link in self.links :
            link.move()
            '''
    '''        
    def itemChange(self, change, variant):
        #if change != QGraphicsItem.ItemSelectedChange:
        self.emit(signalChanged,self.pos())
        return QtGui.QGraphicsTextItem.itemChange(self, change, variant)
       ''' 
    def mouseDoubleClickEvent(self, event):
        self.onExecuteDialog()
    
    def setBrush(self, value) :
        self.brush = value
        
    def keyPressEvent(self, event):
        factor = 8
        x = self.x()
        y = self.y()
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            if event.key() == QtCore.Qt.Key_Left:
                x -= factor
            elif event.key() == QtCore.Qt.Key_Right:
                x += factor
            elif event.key() == QtCore.Qt.Key_Up:
                y -= factor
            elif event.key() == QtCore.Qt.Key_Down:
                y += factor
            self.setPos(QtCore.QPointF(x, y))
            self.update()
        else:
            QtGui.QGraphicsItem.keyPressEvent(self, event)

    def onUpdateGui(self):
        self.update()    

    def boundingRect(self):
        return self.Rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.Rect)
        return path

    def focusInEvent(self, event) :
        super(NodeGui, self).focusInEvent(event)
        self.emit(signalFocusIn, self)

    def paint(self, painter, option, widget=None):
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setBrush(QtGui.QBrush(self.node.color))
        painter.drawRect(self.Rect)
        painter.setFont(QtGui.QFont('Arial', pointSize=16))
        painter.drawText(self.NameRect, QtCore.Qt.AlignCenter, self.node.name) 
        if self.hasFocus() :
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(255,0,0)), 3))
            painter.drawRect(self.Rect.adjusted(2, 2, -2, -2))
        
        painter.setFont(QtGui.QFont('Arial', pointSize=12))
        infoText = 'Storage: {0}\n '.format(len(self.node.storage))
        demandsText = []
        demandsDict = self.node.getDemands()
        if demandsDict != {} :
            for name,count in demandsDict.items() :
                demandsText.append('{0} - {1} '.format(name, count))
            infoText+='\nDemands:\n'+'\n'.join(demandsText)
        painter.drawText(self.InfoRect, QtCore.Qt.AlignCenter, infoText)
        
        if len(self.node.entered) != 0 :
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255,0,0)))
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(255,0,0)), 3))
            painter.drawEllipse(self.Rect.bottomRight()-QtCore.QPointF(15, 15),10,10)
               
        
    def onExecuteDialog(self):
        self.mainwidget.onUpdateLists()
        self.mainwidget.exec_()

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
