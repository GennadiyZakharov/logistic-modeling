
from PyQt4 import QtCore
from cStringIO import StringIO
from lgcore.lglink import LgLink
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.lgplayer import LgPlayer
from lgcore.signals import signalTransport, signalNextTurn
from xml.etree.cElementTree import ElementTree, Element, tostring

class LgModel(QtCore.QObject):
    '''
    This is holder class for all logistic system
    It contains all nodes, links and packages
     Lgmodel is parent for all lg items
    
    It also  contains all payed data
    '''
    def __init__(self):
        super(LgModel, self).__init__()
        self.clear()   
        # FIXME: remove stub     
        teacher = LgPlayer('Teacher',self)
        self.addPlayer(teacher)
        
    def clear(self):
        self.players = []
        
        self.links = set()
        self.nodes = set()
        self.packages = set()
    
    def addPlayer(self, player):
        player.setParent(self)
        self.players.append(player)
    
    def delPlayer(self, player):
        player.setParent(None)
        for node in self.nodes :
            node.viewers.discard(player)
            if node.owner is player :
                node.setOwner(None)
        self.players.remove(player)
    
    def addNode(self, node):
        node.setParent(self)
        self.nodes.add(node)
        
    def delNode(self, node):
        node.setParent(None)
        node.setOwner(None)
        linkstodel = set()
        print "node to delete"
        print self.nodes
        print self.links
        for link in self.links :
            if (node is link.input) or (node is link.output):
                linkstodel.add(link)
        for link in linkstodel :
            self.delLink(link)         
        
        self.nodes.remove(node)
        
        print self.nodes
        print self.links
        
    def addLink(self, link):
        link.setParent(self)
        self.links.add(link)
    
    def delLink(self, link):
        link.setParent(None)
        link.removeOwner()
        link.input.delLink(link)
        self.disconnect(self.input, signalTransport, self.onAddPackage)
        self.disconnect(self, signalTransport, self.output.onPackageEntered)
        self.links.remove(link)
    
    def onNextTurnPressed(self):
        for player in self.players :
            player.onNextTurn()
                
    def toXML(self):
        def indent(elem, level=0):
            i = "\n" + level*"  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                for e in elem:
                    indent(e, level+1)
                    if not e.tail or not e.tail.strip():
                        e.tail = i + "  "
                if not e.tail or not e.tail.strip():
                    e.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i
                    
        modelElement = Element('model')
        # Add players
        playerListElement = Element('playerList')
        for player in self.players:
            playerElement = Element('player', {'name': player.name, 'money': str(player.money)})
            playerListElement.append(playerElement)
        modelElement.append(playerListElement)
        # Add nodes
        nodeListElement = Element('nodeList')
        for node in self.nodes:
            nodeElement = Element('node', {'name': node.name, 
                                           'capacity': str(node.storageCapacity), 
                                           'color': str(node.color.name())})
            # Add packages from storage
            storagePackagesListElement = Element('storagePackagesList')
            for package in node.storage:
                packageElement = Element('package', {'name': package.name})
                storagePackagesListElement.append(packageElement)
            # Add packages from entered
            enteredPackagesListElement = Element('enteredPackagesList')
            for package in node.entered:
                packageElement = Element('package', {'name': package.name})
                enteredPackagesListElement.append(packageElement)           
            # TODO: Add factories
            factoryListElement = Element('factoryList')
            for factory in node.factories:
                factoryElement = Element('factory', {'name': factory.name, 
                                                     'activationInterval': str(factory.activationInterval),
                                                     'currentTurn': str(factory.currentTurn)})
                # Consume
                consumeListElement = Element('consumeList')
                for name, value in factory.consumes.items():
                    consumeElement = Element('consume', {'name': str(name), 'mean': str(value[0]), 'variance': str(value[1])})
                    consumeListElement.append(consumeElement)
                factoryElement.append(consumeListElement)
                # Produce
                produceListElement = Element('produceList')
                for name, value in factory.produces.items():
                    produceElement = Element('produce', {'name': str(name), 'mean': str(value[0]), 'variance': str(value[1])})
                    produceListElement.append(produceElement)
                factoryElement.append(produceListElement)
                # Demand
                demandListElement = Element('demandList')
                for name, value in factory.demands.items():
                    demandElement = Element('demand', {'name': str(name), 'value': str(value)})
                    demandListElement.append(demandElement)
                factoryElement.append(demandListElement)
                # Append factory to list
                factoryListElement.append(factoryElement)
            nodeElement.append(factoryListElement)
            nodeListElement.append(nodeElement)
        modelElement.append(nodeListElement)
        # Add links
        linkListElement = Element('linkList')
        for link in self.links:
            linkElement = Element('link', {'inputName': link.input.name, 
                                           'outputName': link.output.name,
                                           'length': str(link.length),
                                           'maxCapacity': str(link.maxCapacity),
                                           'color': str(link.color.name())})
            packageListElement = Element('packageList')
            for package, position in link.packages.items():
                packageElement = Element('package', {'name': package.name, 'position': str(position)})
                packageListElement.append(packageElement)
            linkElement.append(packageListElement)
            linkListElement.append(linkElement)
        modelElement.append(linkListElement)
        indent(modelElement)
        return tostring(modelElement)
    
    def fromXML(self, source):
        self.clear()
        tree = ElementTree()
        tree.parse(source)
        modelElement = tree.getroot()
        # Read players
        playerListElement = modelElement.find('playerList')
        for playerElement in list(playerListElement):
            player = LgPlayer(playerElement.get('name'), parent=self, money=playerElement.get('money'))
            self.addPlayer(player)
        # TODO: Read nodes
        # TODO: Read factories        
        
    def openModel(self, filename):
        self.fromXML(filename)
         
    def saveModel(self, filename):
        with open(filename, 'w') as f:
            print self.toXML()
            f.write(self.toXML())
        #tree.dump(tree.getroot())                
        #tree.write(filename)
    
    def getData(self):        
        return self.toXML()
    
    def setData(self, data):
        fileStub = StringIO()
        fileStub.write(data)
        self.fromXML(fileStub)
    
    def isFinished(self):
        # TODO: Implement
        pass
        
