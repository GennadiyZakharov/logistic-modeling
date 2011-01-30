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

# ==== Custom signals ====

signalNodeMoved = SIGNAL("nodeMoved")
