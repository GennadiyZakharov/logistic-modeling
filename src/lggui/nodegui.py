from PyQt4 import QtCore, QtGui
from lgcore.signals import signalUpdateGui, signalClicked, signalNextTurnNode
from lggui.nodewidget import NodeWidget

class NodeGui(QtGui.QGraphicsObject):
    '''This class containes all gui functionality for node'''
    Rect = QtCore.QRectF(0, 0, 80, 70)
    
    def __init__(self, node, position, parent=None, scene=None):
        
        super(NodeGui, self).__init__(parent)
        #QtCore.QObject.__init__(self) 
        
        self.node = node
        self.connect(self.node, signalUpdateGui, self.on_updateGui)
        self.connect(self.node, signalNextTurnNode, self.on_AssignItems)
        
        self.color = QtGui.QColor(195, 217, 255)
        self.setPos(position)

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
        #dialog = TextItemDlg(self, self.parentWidget())
        #dialog.exec_()
        self.mainwidget.exec_()
        self.update()
    
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

    def on_updateGui(self):
        pass    

    def boundingRect(self):
        return self.Rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.Rect)
        return path


    def paint(self, painter, option, widget=None):
        painter.setPen(QtCore.Qt.SolidLine)
        painter.setBrush(QtGui.QBrush(self.color))
        painter.drawRect(self.Rect)
        painter.drawText(QtCore.QPoint(10,10),self.node.caption)
        if self.hasFocus() :
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(255,0,0)), 3))
            painter.drawRect(self.Rect.adjusted(2, 2, -2, -2))
            
        if len(self.node.entered) != 0 :
            painter.setBrush(QtGui.QBrush(QtGui.QColor(255,0,0)))
            painter.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(255,0,0)), 3))
            painter.drawEllipse(self.Rect.bottomRight()-QtCore.QPointF(15, 15),10,10)
            
        
    def on_AssignItems(self):
        self.mainwidget.on_Update()
        self.mainwidget.exec_()
        
        pass

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