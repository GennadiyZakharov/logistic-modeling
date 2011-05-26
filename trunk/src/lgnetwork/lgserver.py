from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

class LgServer(object):
    class ClientThread(Thread):
        def __init__(self, channel, details):
            self.channel = channel
            self.details = details
            Thread.__init__(self)
    
        def run ( self ):
            print 'Received connection:', self.details [0]
            for x in xrange(10):
                print self.channel.recv(1024)
                self.channel.send('Hello %i' % x)
            self.channel.close()
            print 'Closed connection:', self.details [0]        
            
    def createGame(self):
        print socket, AF_INET, SOCK_STREAM
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(('', 9000))
        s.listen(5)        
        while True:
            channel, details = s.accept()
            self.ClientThread(channel, details).start()
            
s = LgServer()
s.createGame()
