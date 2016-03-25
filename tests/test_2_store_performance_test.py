from pyspace import Space, Actor
import random
import datetime


class SetActor(Actor):
    def myHandler(self, node, msg):
        if msg[1] == "setStore":
            node.store["store"] = msg[2]
            self | ["request","send", msg[3]]
        elif msg[1] == "send":
            store = self.space.getNode(node.store["store"])
            store | ["store", "add", ["key", random.randrange(0,123123)]]
            if msg[2] > 0:
                count = msg[2]
                count -= 1
                self | ["request","send", count]
            else:
                print "finish %s" % self.getLocation()

    def init(self):
        self.addHandler("request",self.myHandler)

if __name__ == '__main__':
    space = Space()
    n = space.connectToLocation("store@127.0.0.1:20000")

    total = 0
    times = 0
    for i in range(1,100):
        t1 = datetime.datetime.now()
        #n | ["store", "add", ["key","aaa"]]
        n.send_sync(["store", "add", ["key","aaa"]])
        t2 = datetime.datetime.now()
        total += (t2-t1).microseconds
        times += 1
    n | ["store", "add", ["done","1"]]
    print("Store - Add async: avg %s total %s" % (total / times, total))
    #time.sleep(2)

    total = 0
    times = 0
    for i in range(1,1000):
        t1 = datetime.datetime.now()
        n.send_sync(["store", "add", ["key","aaa"]])
        t2 = datetime.datetime.now()
        total += (t2-t1).microseconds
        times += 1
    print("Store - Add sync: avg %s total %s" % (total / times, total))

    total = 0
    times = 0
    for i in range(1,1000):
        t1 = datetime.datetime.now()
        n.send_sync(["store", "get", "key"])
        t2 = datetime.datetime.now()
        total += (t2-t1).microseconds
        times += 1
    print("Store - Get: avg %s total %s" % (total / times, total))