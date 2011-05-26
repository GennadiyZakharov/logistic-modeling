from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class LgClient(object):
    def __init__(self):
        pass
    
    class ConnectionThread(Thread): 
        def __init__(self, serverAddress, serverPort):
            self.serverAddress = serverAddress
            self.serverPort = serverPort
            Thread.__init__(self)
               
        def run(self):    
            # Connect to the server:
            client = socket(AF_INET, SOCK_STREAM)
            client.connect((self.serverAddress, self.serverPort))
            # Send some messages:
            for x in xrange(10):
                client.send('Hey. ' + str(x) + '\n')
                print client.recv(1024)    
                # Close the connection
            client.close()

    def connect(self, serverAddress, serverPort):
        self.ConnectionThread(serverAddress, serverPort).start()

c = LgClient()
c.connect('localhost', 9000)