from PyQt4 import QtCore, QtGui

class LgActions(QtCore.QObject):
    '''
    This class is used to store all application actions. 
    It is Used from mainWinow class
    '''
    
    def __init__(self, parent=None):
        super(LgActions, self).__init__(parent)
        
        # Creating actions
        # ==== file actions
        self.fileNewAction = self.createAction("&New...", QtGui.QKeySequence.New,
                                               "filenew", "Create new task")
        self.fileOpenAction = self.createAction("&Open...",
                                                QtGui.QKeySequence.Open, "fileopen", "Open task")
        self.fileSaveAction = self.createAction("&Save",
                                                QtGui.QKeySequence.Save, "filesave", "Save task")
        self.fileSaveAsAction = self.createAction("Save &as...",
                                                  QtGui.QKeySequence.SaveAs, "filesaveas", "Save task as")
        self.fileConnectAction = self.createAction("Connect...",
                                                  None, "fileconnect", "Connect to server")
        self.fileQuitAction = self.createAction("&Exit",
                                                QtGui.QKeySequence.Quit, "filequit", "Close the application")
        
        self.fileActionsEditor = (self.fileNewAction, self.fileOpenAction, self.fileSaveAction,
                                  self.fileSaveAsAction, None, self.fileQuitAction)
        self.fileActionsPlayer = (self.fileOpenAction, self.fileConnectAction, self.fileSaveAsAction, None, self.fileQuitAction)
        
        '''
        # ==== Mode actons
        self.editModeAction = self.createAction("&Edit Mode", "Ctrl+E" , "modeedit",
                                                "Switch to edit mode", True)
        self.playModeAction = self.createAction("P&lay Mode", "Ctrl+L" , "modeplay",
                                                "Switch to play mode", True)
        editGroup = QtGui.QActionGroup(self)
        editGroup.addAction(self.editModeAction)
        editGroup.addAction(self.playModeAction)
        self.editModeAction.setChecked(True)
        self.modeActions = (self.editModeAction, self.playModeAction) 
        '''
        # ---- Item Actions
        self.addNodeAction = self.createAction("Add node",
                            None, "addnode", "Add node")
        self.editNodeAction = self.createAction("Edit node",
                            None, "editnode", "Edit node")
        self.addLinkAction = self.createAction("Add link",
                            None, "addlink", "Add link")
        self.editLinkAction = self.createAction("Edit link",
                            None, "editlink", "Edit link")
        self.delObjectAction = self.createAction("Delete object",
                            None, "delete", "Delete object")
        
        self.itemActions = (self.addNodeAction, self.editNodeAction, None,
                            self.addLinkAction, self.editLinkAction, None, 
                            self.delObjectAction)
        # ---- Help actions
        self.helpAboutAction = self.createAction("About",
                            QtGui.QKeySequence.HelpContents, "helpabout", "About Logistic Modeller") 
        self.helpActions = (self.helpAboutAction,)
        
        # This method can help in action adding
    def createAction(self, text, shortcut=None, icon=None,
                    tip=None, checkable=False):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)  
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
                
    
        
