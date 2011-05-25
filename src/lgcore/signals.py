from PyQt4.QtCore import SIGNAL

# Standard QT signals
signalClicked = SIGNAL("clicked()")
signalValueChanged = SIGNAL("valueChanged(int)")
signalStateChanged = SIGNAL("stateChanged(int)")
signalTriggered = SIGNAL("triggered()")
signalAccepted = SIGNAL("accepted()")
signalRejected = SIGNAL("rejected()")


signalChanged = SIGNAL('changed') 

signalxChanged = SIGNAL('xChanged()') 
signalyChanged = SIGNAL('yChanged()')


# ==== Custom signals ====
# ---- Core signals ----
signalNextTurn = SIGNAL("nextTurn")
signalNextTurnLink = SIGNAL("nextTurnLink")

signalCost = SIGNAL("cost(int)")
signalTransport = SIGNAL("transport")

signalUpdateGui = SIGNAL("updateGui")
signalExecuteDialog = SIGNAL("executeDialog")
signalPackageAdded = SIGNAL("packageAdded")
signalPackageRemoved = SIGNAL("packageRemoved")

# ---- GUI signals ----
signalNodeMoved = SIGNAL("nodeMoved()")
signalItemMoved = SIGNAL("itemMoved")
signalFocusIn = SIGNAL("focusIn")

