import pickle
import socket
import threading
import SocketServer as SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """ (node, sender, cmd, msg) """
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.currentThread()
        transport = pickle.loads(data)
        #response = "%s: %s.... %s" % (cur_thread.getName(), data, msg) 
        #self.request.send(response)
        #print(transport)
        if transport[3]:
            output = self.server.node.send_sync(transport[2])
            self.request.send(pickle.dumps(output))
            return output
        else:
            self.server.node | transport[2]

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def setNode(self, node):
        self.node = node
