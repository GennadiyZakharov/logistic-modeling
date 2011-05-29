from __future__ import division
from PyQt4 import QtCore, QtGui
from lgcore.lglink import LgLink
from lgcore.signals import signalTriggered, signalClicked, signalFocusIn, \
    signalItemMoved, signalValueChanged
from lggraphicsscene import LgGraphicsScene
from lggui.lgactions import LgActions
from lggui.linkaddwidget import LinkAddWidget
from lggui.linkeditwidget import LinkEditWidget
from lggui.linkgui import LinkGui
from lggui.nodeeditwidget import NodeEditWidget
from lggui.nodegui import NodeGui
from lggui.playerdockwidget import PlayerDockWidget
from lggui.viewdockwidget import ViewDockWidget
import sys



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.__version__ = 0.5
        self.lgActions = LgActions(self)
        
        self.setWindowTitle("Logistic modeling")
        self.setObjectName("MainWindow")
        self.dirty = False
        self.fileName = None        
        
        # ==== Creating main view
        self.scene = LgGraphicsScene(self)
        self.view = QtGui.QGraphicsView()
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setScene(self.scene)
        self.view.setMinimumSize(640, 480) 
        self.setCentralWidget(self.view) 
        # Creating toolbars
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.lgActions.addActions(fileToolbar, self.lgActions.fileActionsEditor)
        editToolbar = self.addToolBar("File")
        editToolbar.setObjectName("EditToolBar")
        self.lgActions.addActions(editToolbar, self.lgActions.itemActions)
        #Creating player dockbar
        playerDockBar = QtGui.QDockWidget("Players", self) # Created and set caption
        playerDockBar.setObjectName("PlayersDockBar")
        playerDockBar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        playerDockBar.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, playerDockBar)
        self.playerDockWidget = PlayerDockWidget(self.scene.model, self) 
        playerDockBar.setWidget(self.playerDockWidget)  
        #Creating view dockbar
        viewDockBar = QtGui.QDockWidget("View control", self) # Created and set caption
        viewDockBar.setObjectName("viewDockWidget")
        viewDockBar.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        viewDockBar.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, viewDockBar)
        self.viewDockWidget = ViewDockWidget() 
        viewDockBar.setWidget(self.viewDockWidget)
        self.connect(self.viewDockWidget.zoomSpinBox, signalValueChanged, self.onScale)    
        # ==== Creating Menu
        # ---- File menu
        fileMenu = self.menuBar().addMenu("&File")
        self.lgActions.addActions(fileMenu, self.lgActions.fileActionsEditor)
        self.connect(self.lgActions.fileOpenAction, signalTriggered, self.fileOpen)
        self.connect(self.lgActions.fileSaveAction, signalTriggered, self.fileSave)
        self.connect(self.lgActions.fileSaveAsAction, signalTriggered, self.fileSaveAs)
        self.connect(self.lgActions.fileQuitAction, signalTriggered, self.close)
        
        # ---- Item Menu ----
        itemMenu = self.menuBar().addMenu("&Item")
        self.lgActions.addActions(itemMenu, self.lgActions.itemActions)
        self.connect(self.lgActions.addNodeAction, signalTriggered, self.onAddNode)
        self.connect(self.lgActions.editNodeAction, signalTriggered, self.onEditNode)
        self.connect(self.lgActions.addLinkAction, signalTriggered, self.onAddLink)
        self.connect(self.lgActions.editLinkAction, signalTriggered, self.onEditLink)
        self.connect(self.lgActions.delObjectAction, signalTriggered, self.onDelObject)
        
        # ----Help menu
        helpMenu = self.menuBar().addMenu("&Help")
        self.lgActions.addActions(helpMenu, self.lgActions.helpActions)
        self.connect(self.lgActions.helpAboutAction, signalTriggered, self.onHelpAbout)
        
        
    # ==== Slots and handlers to handle actions ====
    def onScale(self, value):
        transform = QtGui.QTransform()
        transform.scale(value/100, value/100)
        self.view.setTransform(transform)

    def fileSave(self):
        print self.dirty
        if not self.dirty :
            return
        if self.fileName is None :
            self.fileSaveAs()
        else :
            self.scene.model.saveModel(self.fileName)
            self.dirty = False
    
    def fileOpen(self):
        fname = self.fileName if self.fileName is not None else "."
        formats = ["*.lgmodel"]
        # Invoking dialog
        fname = unicode(QtGui.QFileDialog.getOpenFileName(self,
                            "LgModeller - Open model", fname,
                            "Logistic models (%s)" % " ".join(formats)))
        if fname:
            # Default ext
            if "." not in fname:
                fname += ".lgmodel"
        self.fileName = fname
        self.scene.model.openModel(self.fileName)
        self.scene.updateFromModel()
        self.view.fitInView(self.scene.itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
        self.playerDockWidget.onUpdateList()
    
    def fileSaveAs(self):
        if not self.dirty:
            return
        fname = self.fileName if self.fileName is not None else "."
        formats = ["*.lgmodel"]
        # Invoking dialog
        fname = unicode(QtGui.QFileDialog.getSaveFileName(self,
                            "LgModeller - Save model", fname,
                            "Logistic models (%s)" % " ".join(formats)))
        if fname:
            # Default ext
            if "." not in fname:
                fname += ".lgmodel"
        # Saving file
        # self.addRecentFile(fname)
        self.fileName = fname
        self.fileSave()
    
    def onAddNode(self):
        self.addEditNode(None)
        self.dirty = True
        
    def onEditNode(self):
        if isinstance(self.scene.activeObject, NodeGui) :
            self.addEditNode(self.scene.activeObject.node)
            self.dirty = True
            
    def onAddLink(self):
        self.addEditLink(None)
        self.dirty = True
    
    #-----    
    def onEditLink(self):
        if isinstance(self.scene.activeObject, LinkGui) :
            self.addEditLink(self.scene.activeObject.link)
            self.dirty = True
    
    def addEditNode(self, node):
        dialog = NodeEditWidget(self.scene.model, node, self)
        if dialog.exec_() :
            if node is None :
                # dialog.node.pos = 
                self.scene.model.addNode(dialog.node)
                self.scene.addGNode(dialog.node)
    
    def addEditLink(self, link):
        addLink = False
        if link is None :
            dialog = LinkAddWidget(self.scene.model, self)
            if dialog.exec_() :
                link = LgLink(dialog.input, dialog.output)
                addLink = True
            else :
                return
        dialog = LinkEditWidget(self.scene.model, link, self)
        if dialog.exec_() :
            if addLink :
                #print dialog.link
                self.scene.model.addLink(dialog.link)
                self.scene.addGLink(dialog.link)
    
    def onDelObject(self):
        if isinstance(self.scene.activeObject, NodeGui) :
            self.scene.delGNode(self.scene.activeObject)
            self.dirty = True
            self.scene.activeObject = None
        elif isinstance(self.scene.activeObject, LinkGui) :
            self.scene.delGLink(self.scene.activeObject)
            self.dirty = True
            self.scene.activeObject = None
     
    # Close Event handler
    def closeEvent(self, event):
        # Asking user to confirm
        if self.okToContinue():
            # Saving settings
            settings = QtCore.QSettings()            
            event.accept()
        else:
            event.ignore()  
            
    def onHelpAbout(self):
        QtGui.QMessageBox.about(self, "About Logistic Modeller",
        """<b>Logistic Modeller</b> v %s
        <p>Co.
        Publishe under GNU GPL v3.0.
        <p>Python %s - Qt %s - PyQt %s""" % (
                        self.__version__, sys.platform,
                        QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR))
    
    def okToContinue(self):
        if self.dirty:
            reply = QtGui.QMessageBox.question(self,
                                         "Lg Modeller",
                                         "Save unsaved changes?",
                                         QtGui.QMessageBox.Yes | QtGui.QMessageBox.No | 
                                         QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                self.fileSave()
        return True
    

            
    
            
            
