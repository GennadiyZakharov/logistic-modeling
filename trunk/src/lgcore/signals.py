from PyQt4.QtCore import SIGNAL

# Standard QT signals
signalClicked = SIGNAL("clicked()")
signalValueChanged = SIGNAL("valueChanged(int)")
signalStateChanged = SIGNAL("stateChanged(int)")
signalTriggered = SIGNAL("triggered()")

signalChanged = SIGNAL('changed') 

signalxChanged = SIGNAL('xChanged()') 
signalyChanged = SIGNAL('yChanged()')


# ==== Custom signals ====
# ---- Core signals ----
signalNextTurnLink = SIGNAL("nextTurnLink")
signalNextTurnNode = SIGNAL("nextTurnNode")

signalCost = SIGNAL("cost(int)")
signalTransport = SIGNAL("transport")

signalUpdateGui = SIGNAL("updateGui")
signalPackageAdded = SIGNAL("packageAdded")
signalPackageRemoved = SIGNAL("packageRemoved")

# ---- GUI signals ----
signalNodeMoved = SIGNAL("nodeMoved()")

