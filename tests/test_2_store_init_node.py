from pyspace import Space
from pyspace.node import Store

if __name__ == '__main__':
    space = Space()
    n1 = Store("store", "127.0.0.1", 20000)
    space.spawnNode(n1)
    print "spawned"