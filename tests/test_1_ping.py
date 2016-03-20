from pyspace import LocalNode, Space, RemoteNode

def PingHandler(sender, msg):
    print("Ping! %d" % msg[1])
    sender.space.getNode(msg[2]) | ['pong', msg[1], sender.getLocation()]

def PongHandler(sender, msg):
    print("Pong! %d" % msg[1])
    if msg[1] > 0:
        sender.space.getNode(msg[2]) | ['ping', msg[1]-1, sender.getLocation()]

if __name__ == '__main__':
    n1 = LocalNode("node1", "127.0.0.1", 12344)
    n1.addHandler('ping', PingHandler)
    
    space = Space()
    space.spawnNode(n1)

    n1 | ["ping", 5, "node2@127.0.0.1:12346"]
