from pyspace.node import LocalNode
from pyspace import Space
import time

if __name__ == '__main__':
    n2 = LocalNode("node2", "127.0.0.1", 12350)
    
    s = Space()
    s.addNode(n2)
    s.spawnNode(n2)
    
#    n2 | ["store", "news", n1.getLocation()]
    n2 | ["store","add",["key22", "232g24g24"]]
    time.sleep(3)
    print(n2.send_sync(["store", "add", ["key1", "value2"]]))
    print(n2.send_sync(["store", "get", "key1"]))
    print(n2.send_sync(["store", "get", "key22"]))
    print(n2.store)
    input()