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
        
            
        