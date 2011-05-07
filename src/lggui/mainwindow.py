import sys
from PyQt4 import QtCore, QtGui

from lgcore.signals import signalTriggered, signalClicked
from lgcore.lgactions import LgActions
from lgcore.lgnode import LgNode
from lgcore.lglink import LgLink
from lgcore.lgpackage import LgPackage
from lgcore.lgscheme import LgScheme
from lggui.viewdockbar import ViewDockBar
from lggui.toolsdockbar import ToolsDockBar
from lggui.nodegui import NodeGui
from lggui.linkgui import LinkGui
from lggui.nodeaddwidget import NodeAddWidget
from lggraphicsscene import LgGraphicsScene

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.lgActions = LgActions(self)
        
        self.setWindowTitle("Logistic modeling")
        self.setObjectName("MainWindow")
        self.dirty = True
        
        # All nodes and links will be stored in lists
        self.gnodes = {}
        self.glinks = {}
        
        # ==== Creating main graph view
        self.scene = LgGraphicsScene(self)
        #self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.view = QtGui.QGraphicsView()
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setScene(self.scene)
        #self.view.setFocusPolicy(Qt.NoFocus) 
        self.setCentralWidget(self.view) 
             
        #Creating tool dockbar
        toolsDockWidget = QtGui.QDockWidget("Tools", self) # Created and set caption
        toolsDockWidget.setObjectName("toolsDockWidget")
        toolsDockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        toolsDockWidget.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, toolsDockWidget)
        #Populating view dockbar
        self.toolsDockBar = ToolsDockBar() 
        toolsDockWidget.setWidget(self.toolsDockBar)
        
        #Creating view dockbar
        viewDockWidget = QtGui.QDockWidget("View control", self) # Created and set caption
        viewDockWidget.setObjectName("viewDockWidget")
        viewDockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        viewDockWidget.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, viewDockWidget)
        #Populating view dockbar
        self.viewDockBar = ViewDockBar() 
        viewDockWidget.setWidget(self.viewDockBar)
        
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
        
        self.scheme = LgScheme()
        self.connect(self.toolsDockBar.nextTurnButton, signalClicked, self.scheme.on_NextTurnPressed)
        
        self.factory = self.scheme.addNode(caption='Factory')
        self.warehouse = self.scheme.addNode(caption='Warehouse')
        self.shop1 = self.scheme.addNode(caption='Shop1')
        self.shop2 = self.scheme.addNode(caption='Shop2')
        
        self.link1 = self.scheme.addLink(self.factory, self.warehouse, length=5)
        self.link2 = self.scheme.addLink(self.warehouse, self.shop1, length=4)
        self.link3 = self.scheme.addLink(self.warehouse, self.shop2, length=3)
        
        gfactory = self.addGNode(self.factory, QtCore.QPointF(300, 100))
        gwarehouse = self.addGNode(self.warehouse, QtCore.QPointF(300, 400))
        gshop1 = self.addGNode(self.shop1, QtCore.QPointF(100, 600))
        gshop2 = self.addGNode(self.shop2, QtCore.QPointF(500, 600))
        
        self.addGLink(self.link1)
        self.addGLink(self.link2)
        self.addGLink(self.link3)        
                
        self.link1.on_addPackage(LgPackage())
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
        dialog = NodeAddWidget(self)
        dialog.exec_()
    
    def on_AddLink(self):
        pass
    
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
        return gnode
    
    def addGLink(self, link):
        ginput = self.gnodes[link.input]
        goutput = self.gnodes[link.output]
        glink = LinkGui(link, ginput, goutput)
        self.glinks[link] = glink
        self.scene.addItem(glink)
        return glink   
    
    def delGNode(self):
        gNode = self.scene.focusItem()
        if gNode is None :
            return
        self.scene.removeItem(gNode)
        self.gnodes.pop(gNode.node)
        self.scheme.delNode(gNode.node)
    
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
    

            
    
            
            
