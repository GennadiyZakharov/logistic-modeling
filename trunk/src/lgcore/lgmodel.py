
from PyQt4 import QtCore
from PyQt4.QtGui import QColor
from cStringIO import StringIO
from lgcore.lglink import LgLink
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.lgplayer import LgPlayer
from lgcore.signals import signalTransport, signalNextTurn
from xml.etree.cElementTree import ElementTree, Element, tostring
from lgcore.lgfactory import LgFactory
from PyQt4.uic.Compiler.qtproxies import QtGui

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
            storagePackageListElement = Element('storagePackageList')
            for package in node.storage:
                packageElement = Element('package', {'name': package.name})
                storagePackageListElement.append(packageElement)
            nodeElement.append(storagePackageListElement)
            # Add packages from entered
            enteredPackageListElement = Element('enteredPackageList')
            for package in node.entered:
                packageElement = Element('package', {'name': package.name})
                enteredPackageListElement.append(packageElement)           
            nodeElement.append(enteredPackageListElement)
            # Add factories
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
        # Read nodes
        nodeListElement = modelElement.find('nodeList')
        for nodeElement in list(nodeListElement):
            # Storage
            storage = set()
            storagePackageListElement = nodeElement.find('storagePackageList')
            for packageElement in list(storagePackageListElement):
                package = LgPackage(packageElement.get('name'))
                storage.append(package)
            # Entered
            entered = set()
            enteredPackageListElement = nodeElement.find('enteredPackageList')
            for packageElement in list(enteredPackageListElement):
                package = LgPackage(packageElement.get('name'))
                entered.append(package)
            # Factories
            factories = set()
            factoryListElement = nodeElement.find('factoryList')
            for factoryElement in list(factoryListElement):
                # Consumes
                consumes = {}
                consumeListElement = factoryElement.find('consumeList')
                for consumeElement in list(consumeListElement):
                    consumes[consumeElement.get('name')] = (consumeElement.get('mean'),
                                                            consumeElement.get('variance'))
                # Produces
                produces = {}
                produceListElement = factoryElement.find('produceList')
                for produceElement in list(produceListElement):
                    produces[produceElement.get('name')] = (produceElement.get('mean'),
                                                            produceElement.get('variance'))
                # Demands
                demands = {}
                demandListElement = factoryElement.find('demandList')
                for demandElement in list(demandListElement):
                    demands[demandElement.get('name')] = demandElement.get('value')
                # Construct factory
                factory = LgFactory(name=factoryElement.get('name'))
                factory.consumes = consumes
                factory.produces = produces
                factory.demands = demands
                factory.activationInterval = factoryElement.get('activationInterval')
                factory.currentTurn = factoryElement.get('currentTurn')
                factories.add(factory)        
            # Construct node
            node = LgNode(nodeElement.get('name'), nodeElement.get('capacity'), self)
            node.color = QColor(nodeElement.get('color'))
            node.storage = storage
            node.entered = entered
            node.factories = factories
            self.addNode(node)
        # Links
        linkListElement = modelElement.find('linkList')
        for linkElement in list(linkListElement):
            # Packages
            packages = {}
            packageListElement = linkElement.find('packageList')
            for packageElement in list(packageListElement):
                package = LgPackage(packageElement.get('name'))
                packages[package] = packageElement.get('position')       
            input = None
            output = None 
            inputName = linkElement.get('inputName')
            outputName = linkElement.get('outputName')
            for node in self.nodes:
                if node.name == inputName:
                    input = node
                elif node.name == outputName:
                    output = node
            if not input or not output:
                raise Exception('Input or output nodes for link is None!')
            link = LgLink(input, output, linkElement.get('name'), length=linkElement.get('length'), maxCapacity=linkElement.get('maxCapacity'))
            link.packages = packages
            self.addLink(link)
            
    def openModel(self, filename):
        self.fromXML(filename)
         
    def saveModel(self, filename):
        with open(filename, 'w') as f:
            # print self.toXML()
            f.write(self.toXML())
        # TODO: Remove test
        #self.openModel(filename)
        #with open('1%s' % filename, 'w') as f:
        #    print self.toXML()
        #    f.write(self.toXML())
        #tree.dump(tree.getroot())                
        #tree.write(filename)
    
    def getData(self):        
        return self.toXML()
    
    def setData(self, data):
        #fileStub = StringIO()
        #fileStub.write(data)
        #self.fromXML(fileStub)
        self.fromXML(data)
    
    def isFinished(self):
        # TODO: Implement
        pass
        
