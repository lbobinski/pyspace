from pyspace import LocalNode, Space, RemoteNode

def PongHandler(sender, msg):
    print "Pong! %d" % msg[1]
    if msg[1] > 0:
        sender.space.getNode(msg[2]) | ['ping', msg[1]-1, sender.getLocation()]

if __name__ == '__main__':
    n2 = LocalNode("node2", "127.0.0.1", 12346)
    n2.addHandler('pong', PongHandler)
    
    #n1 = RemoteNode("node1", "127.0.0.1", 12345)
    
    space = Space()
    space.spawnNode(n2)
    #space.spawnNode(n1)
    raw_input()