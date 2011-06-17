from PyQt4.QtCore import SIGNAL

# Standard QT signals
signalClicked = SIGNAL("clicked()")
signalValueChanged = SIGNAL("valueChanged(int)")
signalStateChanged = SIGNAL("stateChanged(int)")
signalTriggered = SIGNAL("triggered()")
signalAccepted = SIGNAL("accepted()")
signalRejected = SIGNAL("rejected()")
signalxChanged = SIGNAL('xChanged()') 
signalyChanged = SIGNAL('yChanged()')

signalChanged = SIGNAL('changed') 

# ==== Custom signals ====
# ---- Core model signals ----
signalPrepareNode  = SIGNAL("prepareNode")
signalNextTurnLink = SIGNAL("nextTurnLink") # Special signal to link
signalNextTurnNode = SIGNAL("nextTurnNode") # Next turn -- to player node, packages
signalPlayerTurn   = SIGNAL("playerTurn") # Next turn -- to player node, packages

signalCost = SIGNAL("cost(int)") # Sending cost to owner



signalTransport = SIGNAL("transport") # Transmit package between elements

# ---- GUI signals ----
signalUpdateGui = SIGNAL("updateGui") # reread core object 
signalExecuteDialog = SIGNAL("executeDialog")
signalUpdatePlayerData = SIGNAL("updatePlayerData")

signalNodeMoved = SIGNAL("nodeMoved()")
signalItemMoved = SIGNAL("itemMoved")
signalPackage = SIGNAL("packageMoved")
signalFocusIn = SIGNAL("focusIn")
signalEditNode = SIGNAL("editNode")
signalEditLink = SIGNAL("editLink")


