from PyQt4 import QtCore, QtGui
from lgcore.lglink import LgLink
from lgcore.lgmodel import LgModel
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.signals import signalTriggered, signalClicked, signalFocusIn
from lggraphicsscene import LgGraphicsScene
from lggui.lgactions import LgActions
from lggui.linkaddwidget import LinkAddWidget
from lggui.linkeditwidget import LinkEditWidget
from lggui.linkgui import LinkGui
from lggui.nodeeditwidget import NodeEditWidget
from lggui.nodegui import NodeGui
from lggui.packagegui import PackageGui
from lggui.playerdockwidget import PlayerDockWidget
from lggui.toolsdockwidget import ToolsDockWidget
from lggui.viewdockwidget import ViewDockWidget
import sys


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
        self.connect(self.lgActions.fileSaveAction, signalTriggered, self.fileSave)
        self.connect(self.lgActions.fileQuitAction, signalTriggered, self.close)
        
        # ---- Mode menu 
        modeMenu = self.menuBar().addMenu("&Mode")
        self.lgActions.addActions(modeMenu, self.lgActions.modeActions)
        
        # ---- Item Menu ----
        itemMenu = self.menuBar().addMenu("&Item")
        self.lgActions.addActions(itemMenu, self.lgActions.itemActions)
        self.connect(self.lgActions.addEditNodeAction, signalTriggered, self.onAddEditNode)
        self.connect(self.lgActions.addEditLinkAction, signalTriggered, self.onAddEditLink)
        self.connect(self.lgActions.delObjectAction, signalTriggered, self.onDelObject)
        
        # ----Help menu
        helpMenu = self.menuBar().addMenu("&Help")
        self.lgActions.addActions(helpMenu, self.lgActions.helpActions)
        self.connect(self.lgActions.helpAboutAction, signalTriggered, self.on_HelpAbout)
        
        # TEST: Creating nodes
        self.connect(self.toolsDockWidget.nextTurnButton, signalClicked, self.model.onNextTurnPressed)
        
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
        
        self.addGNode(factory)
        self.addGNode(warehouse)
        self.addGNode(shop1)
        self.addGNode(shop2)
    
        self.addGLink(link1)
        self.addGLink(link2)
        self.addGLink(link3)        
                
        link1.onAddPackage(LgPackage('Linux'))
    # ==== Slots and handlers to handle actions ====

    def fileSave(self):
        self.model.saveModel('model.xml')
    
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
    
    def onAddEditNode(self):
        node = self.activeObject.node if isinstance(self.activeObject ,NodeGui) else None 
        dialog = NodeEditWidget(self.model, node, self)
        if dialog.exec_() :
            if node is None :
                # dialog.node.pos = 
                self.model.addNode(dialog.node)
                self.addGNode(dialog.node)
    
    def onAddEditLink(self):
        if isinstance(self.activeObject ,LinkGui) :
            link = self.activeObject.link
            addLink = False
        else :
            dialog = LinkAddWidget(self.model, self)
            if dialog.exec_() :
                link = LgLink(dialog.input, dialog.output)
                addLink = True
            else :
                return
        dialog = LinkEditWidget(self.model, link, self)
        if dialog.exec_() :
            if addLink :
                #print dialog.link
                self.model.addLink(dialog.link)
                self.addGLink(dialog.link)
    
    def onDelObject(self):
        if isinstance(self.activeObject ,NodeGui) :
            self.delGNode(self.activeObject)
            self.activeObject = None
        elif isinstance(self.activeObject ,LinkGui) :
            self.delGLink(self.activeObject)
            self.activeObject = None
    
    def onChangeFocus(self, object):
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
    
    def addGNode(self, node):
        gnode = NodeGui(node)
        self.gnodes[node] = gnode
        self.scene.addItem(gnode)
        self.connect(gnode, signalFocusIn, self.onChangeFocus)
        return gnode
    
    def addGLink(self, link):
        print 'adding glink'
        ginput = self.gnodes[link.input]
        goutput = self.gnodes[link.output]
        glink = LinkGui(link, ginput, goutput)
        print glink
        self.glinks[link] = glink
        self.scene.addItem(glink)
        self.connect(glink, signalFocusIn, self.onChangeFocus)
        return glink   
    
    def delGNode(self, nodeGui):
        node = nodeGui.node
        self.scene.removeItem(nodeGui)
        self.gnodes.pop(node)
        self.model.delNode(node)
    
    def delGLink(self, linkGui):
        link = linkGui.link
        self.scene.removeItem(linkGui)
        self.gnodes.pop(link)
        self.model.delNode(link)
            
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
    

            
    
            
            
