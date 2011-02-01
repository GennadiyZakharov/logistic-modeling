'''
Created on 30.01.2011

@author: gena
'''

from PyQt4 import QtCore,QtGui

class LgGraphicsScene(QtGui.QGraphicsScene):
    '''
    classdocs
    '''


    def __init__(self,parent=None):
        '''
        Constructor
        '''
        super(LgGraphicsScene, self).__init__()
        
        
    def dropEvent(self, event):
        #item = self.mouseGrabbedItem()
        print "Dropped"
        return super(LgGraphicsScene, self).dropEvent(event)