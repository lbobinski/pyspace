import cPickle as pickle
import socket
import threading

from threading import Thread
from multiprocessing import Process
from Queue import Queue, Empty
from pyspace.server import ThreadedTCPRequestHandler, ThreadedTCPServer

def StoreHandler(node, msg):
    if msg[1] == "add":
        node.store[msg[2][0]] = msg[2][1]
        #print(msg[2][0] + " " + msg[2][1])
        if msg[2][0] == "done":
            print "done"
        
    if msg[1] == "get":
        try:
            return node.store[msg[2]]
        except KeyError:
            return None
        
    if msg[1] == "delete":
        del node.store[msg[2]]

    if msg[1] == "getmsgcount":
        return node.messages_count
        
    if msg[1] == "print":
        print(node.store)

class Node(object):
    def __init__(self, name, host, port, group=None):
        self.name = name
        self.host = host
        self.port = port
        self.isMaster = False
        self.isLocal = True
        self.isRemote = False
        self.group = group
        self.space = None
        self.max_queue_size = 1000
        self.inbox = Queue(self.max_queue_size)
        self.messages_count = 0
        self.store = {}
        self.handler = {}
        self.addHandler("store", StoreHandler)
                
    def setSpace(self, space):
        self.space = space
        
    def getName(self):
        return self.name
    
    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port
    
    def getLocation(self):
        return "%s@%s:%s" % (self.name, self.host, self.port)
    
    def addHandler(self, cmd, fun):
        self.handler[cmd] = fun
    
    def delHandler(self, cmd):
        del self.handler[cmd]

    def getHandlers(self):
        return self.handler

    """
        potential performance issue
        node | [HANDLER, COMMAND, MSG]
    """
    def send_async(self, message):
        #self.inbox.put(message)
        self._processMsg(message, False)
        self.messages_count += 1

    __or__ = send_async

    def send_sync(self, message):
        response = self._processMsg(message, True)
        self.messages_count += 1
        return response
    
class LocalNode(Node, Thread):
    def __init__(self, name, host, port, group=None):
        Thread.__init__(self)
        Node.__init__(self, name, host, port, group)

        self.running = True
        self.server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        self.server.setNode(self)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.host, self.port = self.server.server_address

    def init(self):
        pass
        
    def run(self):
        self._startServer()
        self.init()
        while self.running:
            message = self.inbox.get()
            self._processMsg(message, False)
    
    def _processMsg(self, message, sync):
        cmd = message[0]
        msg = None
        node = "local"
        
        if len(message) == 2:
            msg = message[1]
        if len(message) == 3:
            node = message[2]

        #print "(%s) cmd: %s, msg: %s" % (node, cmd, message)
        if cmd in self.handler:
            response = self.handler[cmd](self, message)
            return response
    
    def _startServer(self):
        self.server_thread.setDaemon(True)
        self.server_thread.start()
  
class RemoteNode(Node, Thread):
    def __init__(self, name, host, port, group=None):
        Thread.__init__(self)
        Node.__init__(self, name, host, port, group)
        self.running = True
        
    def run(self):
        while self.running:
            #message = self.inbox.get()
            try:
                message = self.inbox.get()
                self._processMsg(message, False)
            except Empty:
                pass

    """
        message
            (receiver, sender, message, sync)
    """
    def _processMsg(self, message, sync):
        cmd = message[0]
        msg = None
        node = "local"
        
        if len(message) == 2:
            msg = message[1]
        if len(message) == 3:
            node = message[2]
            
        transport = [self.getLocation(), 'sender', message, sync]

        #print "(%s) cmd: %s, msg: %s" % (node, cmd, msg)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send(pickle.dumps(transport))
        if sync:
            response = sock.recv(1024)
        sock.close()
        
        if sync and response:
            return pickle.loads(response)

class Actor(LocalNode):
    pass

class Store(Actor):
    pass