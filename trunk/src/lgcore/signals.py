'''
Created on 25.01.2011

@author: gena
'''

from PyQt4.QtCore import SIGNAL

# Standard QT signals
signalClicked = SIGNAL("clicked()")
signalValueChanged = SIGNAL("valueChanged(int)")
signalStateChanged = SIGNAL("stateChanged(int)")
signalTriggered = SIGNAL("triggered()")

signalChanged = SIGNAL('changed(QRectF)')  

# ==== Custom signals ====
# ---- Core signals ----
signalNextTurn = SIGNAL("nextTurn()")
signalCost = SIGNAL("cost(int)")

signalNodeMoved = SIGNAL("nodeMoved()")

