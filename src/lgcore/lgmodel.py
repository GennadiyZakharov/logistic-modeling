
from PyQt4 import QtCore
from PyQt4.QtGui import QColor
from PyQt4.uic.Compiler.qtproxies import QtGui
from cStringIO import StringIO
from lgcore.lgfactory import LgFactory
from lgcore.lglink import LgLink
from lgcore.lgnode import LgNode
from lgcore.lgpackage import LgPackage
from lgcore.lgplayer import LgPlayer
from lgcore.signals import signalTransport, signalPrepareNode, \
    signalNextTurnLink, signalNextTurnNode, signalPlayerTurn, signalUpdateGui, signalUpdatePlayerData
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
        self.networkInterface = None
        self.currentPlayerIndex = 0
        
    def clear(self):
        self.players = []        
        self.links = set()
        self.nodes = set()
        self.packages = set()
        self.currentTurn = 0
        self.currentPlayerIndex = 0
    
    def addPlayer(self, player):
        player.setParent(self)
        self.players.append(player)
    
    def delPlayer(self, player):
        player.setParent(None)
        for node in self.nodes :
            node.viewers.discard(player)
            if node.owner is player :
                node.setOwner(None)
        for link in self.links :
            link.viewers.discard(player)
            if link.owner is player :
                link.setOwner(None)
        self.players.remove(player)
    
    def addNode(self, node):
        node.setParent(self)
        self.connect(self,signalPrepareNode,node.onPrepare)
        self.connect(self,signalNextTurnNode,node.onNextTurn)
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
        
        self.disconnect(self,signalPrepareNode,node.onPrepare)
        self.disconnect(self,signalNextTurnNode,node.onNextTurn)
        self.nodes.remove(node)
        
        print self.nodes
        print self.links
        
    def addLink(self, link):
        link.setParent(self)
        self.connect(self,signalNextTurnLink,link.onNextTurn)
        self.links.add(link)
    
    def delLink(self, link):
        link.setParent(None)
        link.removeOwner()
        link.input.delLink(link)
        self.disconnect(self.input, signalTransport, self.onAddPackage)
        self.disconnect(self, signalTransport, self.output.onPackageEntered)
        self.disconnect(self,signalNextTurnLink,link.onNextTurn)
        self.links.remove(link)
    
    def onNextTurn(self):
        self.currentTurn += 1
        print '///// Turn {0} begins \\\\\ '.format(self.currentTurn)
        self.emit(signalPrepareNode)
        self.emit(signalNextTurnLink)
        self.emit(signalNextTurnNode)
        self.emit(signalUpdatePlayerData)       
       
    def onPlayerTurnEnd(self):        
        '''
        Calls when current player ends his turn
        '''
        currentPlayer = self.players[self.currentPlayerIndex]
        print 'Player',self.currentPlayerIndex, 'end his turn'
        if self.networkInterface is None:
            # single player game         
            # Factories and links works
            currentPlayer.onTurn()
            self.onNextTurn()
        else:
            # Client in multiplayer game
            self.networkInterface.send()
            # TODO: GUI to wait for new turn
            self.networkInterface.receive()
            if not self.networkInterface.isFinish:
                currentPlayer.onTurn()                
            else:
                self.channel.close()
            
        
    def startNetworkGame(self):
        '''
        Calls when current player ends his turn
        '''
        self.currentPlayerIndex = 0
        while not self.isFinished():
            for self.currentPlayerIndex in range(len(self.players)):
                print '==== Player {0} turn {1}'.format(self.currentPlayerIndex,self.currentTurn)
                self.networkInterface.processNetworkCommuncation(self.currentPlayerIndex)           
            self.currentTurn += 1
            self.onNextTurn()
        self.networkInterface.endNetworkCommunication()
            
               
    def toXML(self):
        def writeViewersList(viewers):
            viewerListElement = Element('viewerList')
            for viewer in viewers:
                viewerElement = Element('viewer', {'name': viewer.name})
                viewerListElement.append(viewerElement)
            return viewerListElement
        
        def createPackageSetElement(name, packageSet):
            packageListElement = Element(name)
            for package in packageSet:
                packageElement = Element('package', {'name': package.name})
                packageListElement.append(packageElement)
            return packageListElement
        
        def indent(elem, level=0):
            i = "\n" + level * "  "
            if len(elem):
                if not elem.text or not elem.text.strip():
                    elem.text = i + "  "
                for e in elem:
                    indent(e, level + 1)
                    if not e.tail or not e.tail.strip():
                        e.tail = i + "  "
                if not e.tail or not e.tail.strip():
                    e.tail = i
            else:
                if level and (not elem.tail or not elem.tail.strip()):
                    elem.tail = i
                    
        modelElement = Element('model', {'currentPlayer':str(self.currentPlayerIndex)})
        # Add players
        playerListElement = Element('playerList')
        for player in self.players:
            playerElement = Element('player', {'name': str(player.name), 'money': str(player.money)})
            playerListElement.append(playerElement)
        modelElement.append(playerListElement)
        # Add nodes
        nodeListElement = Element('nodeList')
        for node in self.nodes:
            ownerText = node.owner.name if node.owner is not None else '<None>'
            nodeElement = Element('node', {'name': node.name,
                                           'capacity': str(node.storageCapacity),
                                           'color': str(node.color.name()),
                                           'owner': str(ownerText),
                                           'position_x': str(node.pos.x()),
                                           'position_y': str(node.pos.y()),
                                           'cost': str(node.cost)})
            # Add viewers list
           
            nodeElement.append(writeViewersList(node.viewers))
            # Add packages from storage
            storagePackageListElement = createPackageSetElement('storagePackageList', node.storage)
            nodeElement.append(storagePackageListElement)
            # Add packages from entered
            enteredPackageListElement = createPackageSetElement('enteredPackageList', node.entered)
            nodeElement.append(enteredPackageListElement)
            # Add player rules
            ruleListElement = Element('ruleList')
            for name,(link,count) in node.distributeList.items() :
                ruleElement = Element('rule', {'name': name,
                                               'link': link.name,
                                               'count': str(count) })
                ruleListElement.append(ruleElement)
            nodeElement.append(ruleListElement)
            # Distributed packages
            distributedPackagesListElement = Element('distributedPackagesList')
            for link,packageSet in node.linksDict.items() :
                distributedPackagesElement = Element('distributedPackages',{'name':link.name})
                packageSetElement = createPackageSetElement('packageSet', packageSet)
                distributedPackagesElement.append(packageSetElement)
                distributedPackagesListElement.append(distributedPackagesElement)
            nodeElement.append(distributedPackagesListElement)
            # Add factories
            factoryListElement = Element('factoryList')
            for factory in node.factories:
                ownerText = factory.owner.name if factory.owner is not None else '<None>'
                factoryElement = Element('factory', {'name': factory.name,
                                                     'activationInterval': str(factory.activationInterval),
                                                     'currentTurn': str(factory.currentTurn),
                                                     'owner': str(ownerText),
                                                     'cost': str(factory.cost),
                                                     'income': str(factory.income),
                                                     'fee': str(factory.fee)})
                factoryElement.append(writeViewersList(factory.viewers))
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
            ownerText = link.owner.name if link.owner is not None else '<None>'
            linkElement = Element('link', {'name': link.name,
                                           'inputName': link.input.name,
                                           'outputName': link.output.name,
                                           'length': str(link.length),
                                           'maxCapacity': str(link.maxCapacity),
                                           'color': str(link.color.name()),
                                           'owner': str(ownerText),
                                           'cost': str(link.cost)})
            linkElement.append(writeViewersList(link.viewers))
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
        def readViewersList(viewerListElement):
            viewers = set()
            names = set()
            for viewerElement in list(viewerListElement) :
                names.add(viewerElement.get('name'))
            for player in self.players :
                if player.name in names :
                    viewers.add(player)
            return viewers
        
        self.clear()
        tree = ElementTree(file=source)
        # tree.parse(source)
        modelElement = tree.getroot()
        self.currentPlayerIndex = int(modelElement.get('currentPlayer'))
        #self.currentPlayerIndex =
        # Read players
        playerListElement = modelElement.find('playerList')
        for playerElement in list(playerListElement):
            player = LgPlayer(playerElement.get('name'), parent=self, money=int(playerElement.get('money')))
            self.addPlayer(player)
        # Read nodes
        nodeListElement = modelElement.find('nodeList')
        for nodeElement in list(nodeListElement):
            # Storage
            nodeViewers = readViewersList(nodeElement.find('viewerList'))
            storage = set()
            storagePackageListElement = nodeElement.find('storagePackageList')
            for packageElement in list(storagePackageListElement):
                package = LgPackage(packageElement.get('name'))
                storage.add(package)
            # Player Rules
            ruleListElement = nodeElement.find('ruleList')
            rulesDict = {}
            if ruleListElement is not None:
                for ruleElement in list(ruleListElement):
                    rulesDict[ruleElement.get('name')] = (ruleElement.get('link'), int(ruleElement.get('count')))
            # Distributed packages
            distributedPackagesListElement = nodeElement.find('distributedPackagesList')
            distributedPackagesDict = {}
            if distributedPackagesListElement is not None:
                for distributedPackagesElement in list(distributedPackagesListElement) :
                    linkName = distributedPackagesElement.get('name')
                    packageSetElement = distributedPackagesElement.find('packageSet')
                    packageSet = set()   
                    if packageSetElement is not None:
                        for packageElement in list(packageSetElement) :
                            packageSet.add(LgPackage(packageElement.get('name')))
        
                    
                    distributedPackagesDict[linkName]=packageSet
            # Entered
            entered = set()
            enteredPackageListElement = nodeElement.find('enteredPackageList')
            for packageElement in list(enteredPackageListElement):
                package = LgPackage(packageElement.get('name'))
                entered.add(package)
            # Factories
            factories = set()
            factoryListElement = nodeElement.find('factoryList')
            for factoryElement in list(factoryListElement):
                factoryViewers = readViewersList(nodeElement.find('viewerList'))
                # Consumes
                consumes = {}
                consumeListElement = factoryElement.find('consumeList')
                for consumeElement in list(consumeListElement):
                    consumes[consumeElement.get('name')] = (int(consumeElement.get('mean')),
                                                            int(consumeElement.get('variance')))
                # Produces
                produces = {}
                produceListElement = factoryElement.find('produceList')
                for produceElement in list(produceListElement):
                    produces[produceElement.get('name')] = (int(produceElement.get('mean')),
                                                            int(produceElement.get('variance')))
                # Demands
                demands = {}
                demandListElement = factoryElement.find('demandList')
                for demandElement in list(demandListElement):
                    demands[demandElement.get('name')] = int(demandElement.get('value'))
                # Construct factory
                ownerText = factoryElement.get('owner')
                owner = None
                for player in self.players :
                    if ownerText == player.name :
                        owner = player
                        break
                factory = LgFactory(name=factoryElement.get('name'), owner=owner)
                factory.viewers = factoryViewers
                factory.consumes = consumes
                factory.produces = produces
                factory.demands = demands
                factory.activationInterval = int(factoryElement.get('activationInterval'))
                factory.currentTurn = int(factoryElement.get('currentTurn'))
                factory.cost = int(factoryElement.get('cost'))
                factory.income = int(factoryElement.get('income'))
                factory.fee = int(factoryElement.get('fee'))
                factories.add(factory)        
            # Construct node
            ownerText = nodeElement.get('owner')
            owner = None
            for player in self.players :
                if ownerText == player.name :
                    owner = player
                    break
            node = LgNode(nodeElement.get('name'), int(nodeElement.get('capacity')), self, owner=owner)
            node.color = QColor(nodeElement.get('color'))
            node.cost = int(nodeElement.get('cost'))
            x = float(nodeElement.get('position_x'))
            y = float(nodeElement.get('position_y'))
            node.pos = QtCore.QPointF(x, y)  
            node.viewers = nodeViewers
            node.storage = storage
            node.entered = entered
            
            node.tempDistributeList = rulesDict
            node.tempDistributedPackagesDict = distributedPackagesDict
            for factory in factories :
                node.addFactory(factory)
            self.addNode(node)
            print node.distributeList
        # Links
        linkListElement = modelElement.find('linkList')
        for linkElement in list(linkListElement):
            linkViewers = readViewersList(linkElement.find('viewerList'))
            # Packages
            packages = {}
            packageListElement = linkElement.find('packageList')
            for packageElement in list(packageListElement):
                package = LgPackage(packageElement.get('name'))
                packages[package] = int(packageElement.get('position'))       
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
            
            ownerText = linkElement.get('owner')
            owner = None
            for player in self.players :
                if ownerText == player.name :
                    owner = player
                    break
            link = LgLink(input, output, linkElement.get('name'),
                          length=int(linkElement.get('length')), owner=owner,
                          maxCapacity=int(linkElement.get('maxCapacity')))
            link.color = QColor(linkElement.get('color'))
            link.cost = int(linkElement.get('cost'))
            link.packages = packages
            link.viewers = linkViewers
            self.addLink(link)
        
        for node in self.nodes :
            print 'loaded node', node.name
            rulesList = {}
            for name,(linkName,count) in node.tempDistributeList.items():
                for link in node.links:
                    if link.name == linkName:
                        rulesList[name] = (link,count)
            node.distributeList = rulesList
            del node.tempDistributeList   
            #distributedPackagesDict = {}
            for linkName, packageSet in node.tempDistributedPackagesDict.items():
                #print linkName, packageSet
                for link in node.links:
                    if link.name == linkName:
                        node.linksDict[link] = packageSet
            print 'Loaded distributin',node.name
            print node.linksDict
            #node.linksDict = distributedPackagesDict
            del node.tempDistributedPackagesDict
                      
            
    def openModel(self, filename):
        self.fromXML(filename)
         
    def saveModel(self, filename):
        with open(filename, 'w') as f:
            f.write(self.toXML())
    
    def getData(self):        
        return self.toXML()
    
    def setData(self, data):
        fileStub = StringIO(data)
        self.fromXML(fileStub)        
        self.emit(signalUpdateGui)
    
    def isFinished(self):
        # TODO: Implement
        return False
    
    def setNetworkInterface(self, ni):
        self.networkInterface = ni    
