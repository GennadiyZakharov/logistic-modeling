from __future__ import division
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt

class LgGraph(QtCore.QObject):
    def __init__(self, parent=None):
        super(LgGraph, self).__init__(parent)
        self.shiftTo = 0
        #self.clearPlot()
    
    def setTitle(self, title):
        plt.title(title)
        
    def setXLabel(self, xLabel):
        plt.xlabel(xLabel)
    
    def setYLabel(self, yLabel):
        plt.ylabel(yLabel)
        
    def setShiftTo(self, value):
        self.shiftTo = value
    
    def clearPlot(self):
        plt.close('all')  
    
    def plotGraph(self, data, filename):
        #P.xlim(xlimits)
        #P.xticks(xticks)
        
        for name,dataSet in data.items() :
            x = range(self.shiftTo,self.shiftTo+len(dataSet)) 
            print 'Plot',x,dataSet
            plt.plot(x, dataSet,'-bo')
            #fmt=linestyles[i],lw=linewidth,ms=marksize,label=datasettitle)
            # set some legend properties.  All the code below is optional.  The
            # defaults are usually sensible but if you need more control, this
            # shows you how
        plt.savefig(filename,dpi=72,format='png')
        
if __name__ == '__main__' :
    graph = LgGraph()
    #graph.setShiftTo(10)
    graph.plotGraph({'player1':[9,8,7,6,5],'player2':[1,2,3,4,5]}, 'test.png')
        
    