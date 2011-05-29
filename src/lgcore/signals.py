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
signalCost = SIGNAL("cost(int)") # Sending cost to owner
signalNextTurn = SIGNAL("nextTurn") # Next turn -- to player node, packages
signalNextTurnLink = SIGNAL("nextTurnLink") # Special signal to link
signalTransport = SIGNAL("transport") # Transmit package between elements

# ---- GUI signals ----
signalUpdateGui = SIGNAL("updateGui") # reread core object 
signalExecuteDialog = SIGNAL("executeDialog")

signalNodeMoved = SIGNAL("nodeMoved()")
signalItemMoved = SIGNAL("itemMoved")
signalFocusIn = SIGNAL("focusIn")



