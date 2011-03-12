'''
Created on 25.01.2011

@author: gena
'''


#TODO: arrow has to be repainted


#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 13.12.2010

@author: gena
'''
import sys,os

from PyQt4 import QtCore,QtGui

from lgcore.signals import *
from lgcore.lgactions import LgActions
from lggui.viewdockbar import ViewDockBar
from lggui.toolsdockbar import ToolsDockBar

from lggui.nodegui import NodeGui
from lggui.linkgui import LinkGui
from lggraphicsscene import LgGraphicsScene

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''
    __version__ = '0.2'

    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__(parent)
        
        self.lgActions = LgActions(self)
        
        self.setWindowTitle("Logistic modeling")
        self.setObjectName("MainWindow")
        self.dirty = True
        
        # All nodes and links will be stored in lists
        self.nodeslist = []
        self.linkslist = []
        
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
        self.toolsDockBar=ToolsDockBar() 
        toolsDockWidget.setWidget(self.toolsDockBar)
        
        #Creating view dockbar
        viewDockWidget = QtGui.QDockWidget("View control", self) # Created and set caption
        viewDockWidget.setObjectName("viewDockWidget")
        viewDockWidget.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        viewDockWidget.setFeatures(QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, viewDockWidget)
        #Populating view dockbar
        self.viewDockBar=ViewDockBar() 
        viewDockWidget.setWidget(self.viewDockBar)
        
        # ==== Creating Menu
        # ---- File menu
        fileMenu = self.menuBar().addMenu("&File")
        self.lgActions.addActions(fileMenu, self.lgActions.fileActions)
        self.connect(self.lgActions.fileQuitAction, signalTriggered,self.close)
        
        # ---- Mode menu 
        modeMenu = self.menuBar().addMenu("&Mode")
        self.lgActions.addActions(modeMenu, self.lgActions.modeActions)
                
        # ----Help menu
        helpMenu = self.menuBar().addMenu("&Help")
        self.lgActions.addActions(helpMenu, self.lgActions.helpActions)
        self.connect(self.lgActions.helpAboutAction, signalTriggered,self.on_HelpAbout)
                
        testnode1 = NodeGui(QtCore.QPointF(100,100),self,self.scene)
        self.scene.addItem(testnode1)
        testnode2 = NodeGui(QtCore.QPointF(500,300),self,self.scene)
        self.scene.addItem(testnode2)
        
        testlink = LinkGui(testnode1,testnode2,self.scene,self.scene)
        self.scene.addItem(testlink)
        testnode1.addLink(testlink)
        testnode2.addLink(testlink)
        
        self.connect(testnode1, signalxChanged,testlink.move)
        self.connect(testnode1, signalyChanged,testlink.move)
        self.connect(testnode2, signalxChanged,testlink.move)
        self.connect(testnode2, signalyChanged,testlink.move)
        
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
                                         QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|
                                         QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Cancel:
                return False
            elif reply == QtGui.QMessageBox.Yes:
                self.fileSave()
        return True

    # ==== Service Methods
    

            
    
            
            
