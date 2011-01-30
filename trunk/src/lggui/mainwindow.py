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
from lggui.viewdockbar import ViewDockBar
from lggui.toolsdockbar import ToolsDockBar

from lggui.nodegui import NodeGui
from lggui.linkgui import LinkGui

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''

    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(MainWindow, self).__init__(parent)
        
        self.setWindowTitle("Logistic modeling")
        self.setObjectName("MainWindow")
        self.dirty = True
        
        # All nodes and links will be stored in lists
        self.nodeslist = []
        self.linkslist = []
        
        # ==== Creating main graph view
        self.scene = QtGui.QGraphicsScene(self)
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
        
        
        # Creating file menu
        fileMenu = self.menuBar().addMenu("&File")
        
        # Creating video menu
        videoMenu = self.menuBar().addMenu("&Video")
                
                
        testnode1 = NodeGui(QtCore.QPointF(100,100),self)
        self.scene.addItem(testnode1)
        testnode2 = NodeGui(QtCore.QPointF(200,200),self)
        self.scene.addItem(testnode2)
        
        testlink = LinkGui(testnode1,testnode2,self)
        self.scene.addItem(testlink)
        testnode1.addLink(testlink)
        testnode2.addLink(testlink)
        
        
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
    
    # This method can help in action adding
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                    tip=None, checkable=False, signal="triggered()"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)  
        if checkable:
            action.setCheckable(True)
        return action
    
    # Method to add All actions from the list
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
            
    
            
            
