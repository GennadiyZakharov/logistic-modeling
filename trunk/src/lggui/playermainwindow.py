from __future__ import division
from PyQt4 import QtCore, QtGui
from lgcore.lglink import LgLink
from lgcore.lgmodel import LgModel
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.signals import signalTriggered, signalClicked, signalFocusIn, \
    signalItemMoved, signalValueChanged
from lggraphicsscene import LgGraphicsScene
from lggui.connectwidget import ConnectWidget
from lggui.gamewidget import GameWidget
from lggui.lgactions import LgActions
from lggui.linkgui import LinkGui
from lggui.nodegui import NodeGui
from lggui.packagegui import PackageGui
from lggui.playerdockwidget import PlayerDockWidget
from lggui.toolsdockwidget import ToolsDockWidget
from lggui.viewdockwidget import ViewDockWidget
import sys



class PlayerMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(PlayerMainWindow, self).__init__(parent)
        self.__version__ = 0.5
        
        self.lgActions = LgActions(self)
        
        self.setWindowTitle("Logistic player")
        self.setObjectName("MainWindow")
        self.fileName = None
        # ==== Creating main graph view
        self.scene = LgGraphicsScene(self)
        self.view = QtGui.QGraphicsView()
        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setScene(self.scene)
        self.view.setMinimumSize(640, 480)
        self.setCentralWidget(self.view) 
        # Creating toolbar
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.lgActions.addActions(fileToolbar, self.lgActions.fileActionsPlayer)
        #Creating player dockbar
        playerDockBar = QtGui.QDockWidget("Players", self) # Created and set caption
        playerDockBar.setObjectName("PlayersDockBar")
        playerDockBar.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        playerDockBar.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, playerDockBar)
        self.playerDockWidget = PlayerDockWidget(self.scene.model, self, False) 
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
        #Creating game dockbar
        gameDockBar = QtGui.QDockWidget("Game control", self) # Created and set caption
        gameDockBar.setObjectName("gameDockBar")
        gameDockBar.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        gameDockBar.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, gameDockBar)
        self.gameWidget = GameWidget() 
        gameDockBar.setWidget(self.gameWidget)
        
        # ==== Creating Menu
        # ---- File menu
        fileMenu = self.menuBar().addMenu("&File")
        self.lgActions.addActions(fileMenu, self.lgActions.fileActionsPlayer)
        self.connect(self.lgActions.fileOpenAction, signalTriggered, self.fileOpen)
        self.connect(self.lgActions.fileConnectAction, signalTriggered, self.fileConnect)
        self.connect(self.lgActions.fileQuitAction, signalTriggered, self.close)
        
        '''
        # ---- Item Menu ----
        itemMenu = self.menuBar().addMenu("&Item")
        self.lgActions.addActions(itemMenu, self.lgActions.itemActions)
        self.connect(self.lgActions.addEditNodeAction, signalTriggered, self.onAddEditNode)
        self.connect(self.lgActions.addEditLinkAction, signalTriggered, self.onAddEditLink)
        self.connect(self.lgActions.delObjectAction, signalTriggered, self.onDelObject)
        '''
        # ----Help menu
        helpMenu = self.menuBar().addMenu("&Help")
        self.lgActions.addActions(helpMenu, self.lgActions.helpActions)
        self.connect(self.lgActions.helpAboutAction, signalTriggered, self.on_HelpAbout)
        
        self.connect(self.gameWidget.nextTurnButton, signalClicked, self.scene.model.onNextTurnPressed)        
        self.scene.updateFromModel()
    # ==== Slots and handlers to handle actions ====

    def onScale(self, value):
        transform = QtGui.QTransform()
        transform.scale(value/100, value/100)
        self.view.setTransform(transform)

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
    
    def fileConnect(self):
        dialog = ConnectWidget(self)
        if dialog.exec_():
            pass
    
    # Close Event handler
    '''
    def closeEvent(self, event):
        # Asking user to confirm
        if self.okToContinue():
            # Saving settings
            settings = QtCore.QSettings()            
            event.accept()
        else:
            event.ignore()      
    '''        
    def on_HelpAbout(self):
        QtGui.QMessageBox.about(self, "About Logistic Modeller",
        """<b>Logistic Modeller</b> v %s
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
    

            
    
            
            

