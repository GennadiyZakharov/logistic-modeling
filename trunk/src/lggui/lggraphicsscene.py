from PyQt4 import QtGui, QtCore
from lgcore.lglink import LgLink
from lgcore.lgmodel import LgModel
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.signals import signalFocusIn, signalItemMoved
from lggui.linkgui import LinkGui
from lggui.nodegui import NodeGui

class LgGraphicsScene(QtGui.QGraphicsScene):
    
    def __init__(self,parent=None):
        super(LgGraphicsScene, self).__init__()
        
        self.model = LgModel()
        
        self.connect(self, signalFocusIn, self.onChangeFocus)
        
    
        # FIXME: remove stub
        factory = LgNode('Factory')
        factory.pos = QtCore.QPointF(300, 100)
        self.model.addNode(factory)
        warehouse = LgNode('Warehouse')
        warehouse.pos = QtCore.QPointF(300, 400)
        self.model.addNode(warehouse)
        shop1 = LgNode('Shop1')
        shop1.pos = QtCore.QPointF(100, 600)
        self.model.addNode(shop1)
        shop2 = LgNode('Shop2')
        shop2.pos = QtCore.QPointF(500, 600)
        self.model.addNode(shop2)
        
        link1 = LgLink(factory, warehouse, 'Road1', length=5)
        self.model.addLink(link1)
        link2 = LgLink(warehouse, shop1, 'Road2', length=4)
        self.model.addLink(link2)
        link3 = LgLink(warehouse, shop2, 'Road3', length=3)
        self.model.addLink(link3)
      
        link1.onAddPackage(LgPackage('Linux'))
    
        self.updateFromModel()
    
    def addGNode(self, node):
        gnode = NodeGui(node)
        self.gnodes[node] = gnode
        self.addItem(gnode)
        self.connect(gnode, signalFocusIn, self.onChangeFocus)
        self.connect(gnode, signalItemMoved, node.onMoved)
        return gnode
    
    def addGLink(self, link):
        ginput = self.gnodes[link.input]
        goutput = self.gnodes[link.output]
        glink = LinkGui(link, ginput, goutput)
        self.glinks[link] = glink
        self.addItem(glink)
        self.connect(glink, signalFocusIn, self.onChangeFocus)
        return glink   
    
    def delGNode(self, nodeGui):
        node = nodeGui.node
        self.removeItem(nodeGui)
        self.gnodes.pop(node)
        self.model.delNode(node)
    
    def delGLink(self, linkGui):
        link = linkGui.link
        self.removeItem(linkGui)
        self.gnodes.pop(link)
        self.model.delNode(link)
        
    def updateFromModel(self):
        self.gnodes = {}
        self.glinks = {}
        self.activeObject=None
        for node in self.model.nodes :
            self.addGNode(node)
        for link in self.model.links :
            self.addGLink(link)
            
    def onChangeFocus(self, object):
        self.activeObject = object
        
            
        