class NetworkCommon(object):
    def __init__(self):
        self.data = None
        self.isFinish = False
    
    def receive(self):
        data = ''
        while True:                
            buff = self.channel.recv(1024)
            data += buff   
            if len(buff) < 1024:
                break                             
        self.data = data
        
    def setIsFinish(self, value):
        self.isFinish = value
        
    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data
        
    def send(self):
        self.channel.send(self.data)    