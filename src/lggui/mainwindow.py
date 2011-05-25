import sys
from PyQt4 import QtCore, QtGui

from lgcore.signals import signalTriggered, signalClicked, signalFocusIn
from lggui.lgactions import LgActions
from lgcore.lgnode import LgNode
from lgcore.lglink import LgLink
from lgcore.lgpackage import LgPackage
from lgcore.lgmodel import LgModel
from lggui.viewdockwidget import ViewDockWidget
from lggui.toolsdockwidget import ToolsDockWidget
from lggui.playerdockwidget import PlayerDockWidget
from lggui.nodegui import NodeGui
from lggui.linkgui import LinkGui
from lggui.nodeeditwidget import NodeEditWidget
from lggraphicsscene import LgGraphicsScene
from lggui.packagegui import PackageGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.model = LgModel()
        
        self.lgActions = LgActions(self)
        
        self.setWindowTitle("Logistic modeling")
        self.setObjectName("MainWindow")
        self.dirty = False
        
        # All nodes and links will be stored in lists
        self.gnodes = {}
        self.glinks = {}
        self.activeObject=None
        
        # ==== Creating main graph view
        self.scene = LgGraphicsScene(self)
        #self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.view = QtGui.QGraphicsView()
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setScene(self.scene)
        #self.view.setFocusPolicy(Qt.NoFocus) 
        self.setCentralWidget(self.view) 
             
        #Creating tool dockbar
        toolsDockBar = QtGui.QDockWidget("Tools", self) # Created and set caption
        toolsDockBar.setObjectName("toolsDockWidget")
        toolsDockBar.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        toolsDockBar.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, toolsDockBar)
        #Populating view dockbar
        self.toolsDockWidget = ToolsDockWidget() 
        toolsDockBar.setWidget(self.toolsDockWidget)
        
        #Creating view dockbar
        viewDockBar = QtGui.QDockWidget("View control", self) # Created and set caption
        viewDockBar.setObjectName("viewDockWidget")
        viewDockBar.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        viewDockBar.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, viewDockBar)
        #Populating view dockbar
        self.viewDockWidget = ViewDockWidget() 
        viewDockBar.setWidget(self.viewDockWidget)
        
        #Creating player dockbar
        playerDockBar = QtGui.QDockWidget("Players", self) # Created and set caption
        playerDockBar.setObjectName("PlayersDockBar")
        playerDockBar.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        playerDockBar.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, playerDockBar)
        #Populating view dockbar
        self.playerDockWidget = PlayerDockWidget(self.model,self) 
        playerDockBar.setWidget(self.playerDockWidget)
        
        
        # ==== Creating Menu
        # ---- File menu
        fileMenu = self.menuBar().addMenu("&File")
        self.lgActions.addActions(fileMenu, self.lgActions.fileActions)
        self.connect(self.lgActions.fileQuitAction, signalTriggered, self.close)
        
        # ---- Mode menu 
        modeMenu = self.menuBar().addMenu("&Mode")
        self.lgActions.addActions(modeMenu, self.lgActions.modeActions)
        
        # ---- Item Menu ----
        itemMenu = self.menuBar().addMenu("&Item")
        self.lgActions.addActions(itemMenu, self.lgActions.itemActions)
        self.connect(self.lgActions.addNodeAction, signalTriggered, self.on_AddNode)
        self.connect(self.lgActions.addLinkAction, signalTriggered, self.on_AddLink)
        self.connect(self.lgActions.delNodeAction, signalTriggered, self.delGNode)
        self.connect(self.lgActions.delLinkAction, signalTriggered, self.delGLink)
        
        # ----Help menu
        helpMenu = self.menuBar().addMenu("&Help")
        self.lgActions.addActions(helpMenu, self.lgActions.helpActions)
        self.connect(self.lgActions.helpAboutAction, signalTriggered, self.on_HelpAbout)
        
        # TEST: Creating nodes
        self.connect(self.toolsDockWidget.nextTurnButton, signalClicked, self.model.onNextTurnPressed)
        
        self.factory = LgNode('Factory', owner=self.model.teacher)
        self.model.addNode(self.factory)
        self.warehouse = LgNode('Warehouse', owner=self.model.teacher)
        self.model.addNode(self.warehouse)
        self.shop1 = LgNode('Shop1', owner=self.model.teacher)
        self.model.addNode(self.shop1)
        self.shop2 = LgNode('Shop2', owner=self.model.teacher)
        self.model.addNode(self.shop2)
        
        self.link1 = LgLink(self.factory, self.warehouse, 'Road1', length=5, owner=self.model.teacher)
        self.model.addLink(self.link1)
        self.link2 = LgLink(self.warehouse, self.shop1, 'Road2', length=4, owner=self.model.teacher)
        self.model.addLink(self.link2)
        self.link3 = LgLink(self.warehouse, self.shop2, 'Road3', length=3, owner=self.model.teacher)
        self.model.addLink(self.link3)
        
        gfactory = self.addGNode(self.factory, QtCore.QPointF(300, 100))
        gwarehouse = self.addGNode(self.warehouse, QtCore.QPointF(300, 400))
        gshop1 = self.addGNode(self.shop1, QtCore.QPointF(100, 600))
        gshop2 = self.addGNode(self.shop2, QtCore.QPointF(500, 600))
        
        self.addGLink(self.link1)
        self.addGLink(self.link2)
        self.addGLink(self.link3)        
                
        self.link1.onAddPackage(LgPackage('Linux'))
    # ==== Slots and handlers to handle actions ====

    def fileSave(self):
        pass
    
    def fileOpen(self):
        pass
    
    def fileSaveAs(self):
        if not self.dirty:
            # Nothing to do
            return
        fname = self.filename if self.filename is not None else "."
        formats = ["*.%s" % unicode(format).lower() \
                   for format in QtGui.QImageWriter.supportedImageFormats()]
        # Invoking dialog
        fname = unicode(QtGui.QFileDialog.getSaveFileName(self,
                                                    "Image Changer - Save Image", fname,
                                                    "Image files (%s)" % " ".join(formats)))
        if fname:
            # Default ext
            if "." not in fname:
                fname += ".png"
        # Saving file
        # self.addRecentFile(fname)
        self.filename = fname
        self.fileSave()
    
    def on_AddNode(self):
        dialog = NodeEditWidget(None, self)
        dialog.exec_()
    
    def on_AddLink(self):
        pass
    
    def onChangeFocus(self, object):
        print object
        self.activeObject = object
    
    # Close Event handler
    def closeEvent(self, event):
        # Asking user to confirm
        if self.okToContinue():
            # Saving settings
            settings = QtCore.QSettings()            
            event.accept()
        else:
            event.ignore()
            
    def nextTurn(self):
        for node in self.nodeslist :
            node.nextTurn()
        
        for link in self.linkslist :
            link.nextTurn()
    
    
    def addGNode(self, node, pos=None):
        gnode = NodeGui(node, pos)
        self.gnodes[node] = gnode
        self.scene.addItem(gnode)
        self.connect(gnode, signalFocusIn, self.onChangeFocus)
        return gnode
    
    def addGLink(self, link):
        ginput = self.gnodes[link.input]
        goutput = self.gnodes[link.output]
        glink = LinkGui(link, ginput, goutput)
        self.glinks[link] = glink
        self.scene.addItem(glink)
        return glink   
    
    def delGNode(self):
        if self.activeObject is None :
            return
        node = self.activeObject.node
        self.scene.removeItem(self.activeObject)
        self.gnodes.pop(node)
        self.model.delNode(node)
        self.activeObject = None
    
    def delGLink(self):
        pass
            
    def on_HelpAbout(self):
        QtGui.QMessageBox.about(self, "About Logistic Modeller",
        """<b>Logistic Modeller</b> v %s
        <p>Copyright &copy; 2007 Qtrac Ltd.
        All rights reserved.
        <p>This application can be used to perform
        simple image manipulations.
        <p>Python %s - Qt %s - PyQt %s""" % (
                        self.__version__, sys.platform,
                        QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR))
    
    
    
    def okToContinue(self):
        if self.dirty:
            reply = QtGui.QMessageBox.question(self,
                                         "Unsaved Changes",
                                         "Save unsaved changes?",
                                         QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | 
                                         QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                self.fileSave()
        return True

    # ==== Service Methods
    

            
    
            
            
