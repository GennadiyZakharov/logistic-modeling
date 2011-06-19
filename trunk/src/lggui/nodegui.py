from __future__ import division
from PyQt4 import QtCore, QtGui
from lgcore.signals import signalUpdateGui, signalClicked, signalExecuteDialog, \
    signalFocusIn, signalItemMoved, signalEditNode
from lggui.nodewidget import NodeWidget

class NodeGui(QtGui.QGraphicsObject):
    '''This class containes all gui functionality for node'''
    Rect = QtCore.QRectF(0, 0, 150, 170)
    NameRect = QtCore.QRectF(0,0,Rect.width(),40)
    InfoRect = QtCore.QRectF(0,50,Rect.width(),100)
    SelectColor = QtGui.QColor(255,0,0)
    InactiveColor = QtGui.QColor(128,128,128)
    
    def __init__(self, node, model, parent=None, scene=None, editMode=False):
        
        super(NodeGui, self).__init__(parent)
        self.node = node
        self.editMode = editMode
        self.model = model
        self.currentPlayer = model.players[model.currentPlayerIndex]
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
        self.onUpdateGui()
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
        if self.editMode :
            self.emit(signalEditNode,self)
        else :
            # Verify for owner
            if self.node.owner == self.currentPlayer:
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
        if self.editMode or (self.currentPlayer in self.node.viewers) :
            toolTip = ('''<b>{0}</b>
                       <br />Storage cost: {1}
                       <br />Waiting for distribute: {2}'''.format(self.node.name,
                                    self.node.cost,len(self.node.entered)))
            factoryTips = []
            for factory in self.node.factories:
                consumesText = '<br />'.join(['{0} - {1}'.format(name,mean) for name,(mean,disp) in factory.consumes.items()])
                produceText = '<br />'.join(['{0} - {1}'.format(name,mean) for name,(mean,disp) in factory.produces.items()])
                tipText = '''<b>{0}</b>
                           <br />Consume income: {1}
                           <br />Produce cost: {2}
                           <br />Indelivering fee: {3}
                           '''.format(factory.name,factory.income,factory.cost,factory.fee)
                if consumesText != '':
                    tipText += '<br />Consumes:<br />' + consumesText 
                if produceText != '':
                    tipText += '<br />Produces:<br />' + produceText
                factoryTips.append(tipText) 
            if len(factoryTips)>0:
                toolTip += '<p text-indent:-.0.5cm><b>Factories:</b><br />'+'<br />'.join(factoryTips)
        else :
            toolTip = 'You are not allowed <br />to see object properties'
        self.setToolTip(toolTip)
        #self.mainwidget.onUpdateLists()
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
        painter.setFont(QtGui.QFont('Arial', pointSize=12))
        if self.currentPlayer in self.node.viewers:
            infoText = 'Storage: {0}/{1}\n '.format(len(self.node.storage),self.node.storageCapacity)
            demandsText = []
            demandsDict = self.node.getDemands()
            if demandsDict != {} :
                for name,count in demandsDict.items() :
                    demandsText.append('{0} - {1} '.format(name, count))
                infoText+='\nDemands:\n'+'\n'.join(demandsText)
            painter.drawText(self.InfoRect, QtCore.Qt.AlignCenter, infoText)
            if len(self.node.entered) != 0 :
                painter.setBrush(QtGui.QBrush(self.SelectColor))
                painter.setPen(QtGui.QPen(QtGui.QBrush(self.SelectColor), 3))
                painter.drawEllipse(self.Rect.bottomRight()-QtCore.QPointF(15, 15),10,10)
        if self.hasFocus() :
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtGui.QBrush(self.SelectColor), 3))
            painter.drawRect(self.Rect.adjusted(2, 2, -2, -2))
        if self.node.owner != self.currentPlayer:
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtGui.QBrush(self.InactiveColor), 3))
            painter.drawRect(self.Rect.adjusted(2, 2, -2, -2))
        
    def onExecuteDialog(self):
        print 'updating lists'
        self.mainwidget.onUpdateLists()
        print 'execute'
        self.mainwidget.exec_()
        self.onUpdateGui()

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
