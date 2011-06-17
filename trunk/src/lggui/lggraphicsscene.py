from PyQt4 import QtGui, QtCore
from lgcore.lglink import LgLink
from lgcore.lgmodel import LgModel
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.signals import signalFocusIn, signalItemMoved, signalEditNode, signalEditLink,\
    signalUpdateGui
from lggui.linkgui import LinkGui
from lggui.nodegui import NodeGui

class LgGraphicsScene(QtGui.QGraphicsScene):
    
    def __init__(self,parent=None, editMode=False):
        super(LgGraphicsScene, self).__init__()
        self.model = LgModel()
        self.connect(self.model, signalUpdateGui, self.updateFromModel)
        self.editMode=editMode
        self.connect(self, signalFocusIn, self.onChangeFocus)
        self.updateFromModel()
    
    def addGNode(self, node):
        gnode = NodeGui(node, self.model, editMode=self.editMode)
        self.gnodes[node] = gnode
        self.addItem(gnode)
        self.connect(gnode, signalFocusIn, self.onChangeFocus)
        self.connect(gnode, signalItemMoved, node.onMoved)
        self.connect(gnode, signalEditNode, self.onChangeFocus)
        self.connect(gnode, signalEditNode, self.onEditNode)
        return gnode
    
    def addGLink(self, link):
        ginput = self.gnodes[link.input]
        goutput = self.gnodes[link.output]
        glink = LinkGui(link, ginput, goutput, self.model, editMode=self.editMode)
        self.connect(glink, signalEditLink, self.onChangeFocus)
        self.connect(glink, signalEditLink, self.onEditLink)
        self.glinks[link] = glink
        self.addItem(glink)
        self.connect(glink, signalFocusIn, self.onChangeFocus)
        return glink   
    
    def delGNode(self, gnode):
        node = gnode.node
        self.disconnect(gnode, signalEditNode, self.onChangeFocus)
        self.disconnect(gnode, signalEditNode, self.onEditNode)
        self.removeItem(gnode)
        self.gnodes.pop(node)
        self.model.delNode(node)
    
    def delGLink(self, glink):
        link = glink.link
        self.disconnect(glink, signalEditLink, self.onChangeFocus)
        self.disconnect(glink, signalEditLink, self.onEditLink)
        self.removeItem(glink)
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
        
    def onEditNode(self):
        self.emit(signalEditNode)
    
    def onEditLink(self):
        self.emit(signalEditLink)
        
            
        