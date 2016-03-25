from pyspace.node import LocalNode, RemoteNode, Actor

__all__ = ['node','server']

class Space(object):
    def __init__(self):
        self.nodes = {}
        self.groups = {}
        
    def addNode(self, node):
        self.nodes[node.getLocation()] = node
        if node.group != None:
            if node.group not in self.groups:
                self.groups[node.group] = [node]

        node.setSpace(self)
                
    def removeNode(self, node):
        del self.nodes[node.getLocation()]
        
    def spawnNode(self, node):
        self.addNode(node)
        node.start()
        
    def getNode(self, location):
        try:
            return self.nodes[location]
        except KeyError:
            return self.connectToLocation(location)
        
    def getNodes(self):
        return self.nodes
    
    def connectToLocation(self, location):
        name = location[:location.find("@")]
        host = location[location.find("@")+1:location.find(":")]
        port = int(location[location.find(":")+1:])
        
        node = RemoteNode(name, host, port)
        self.spawnNode(node)
        
        return node
