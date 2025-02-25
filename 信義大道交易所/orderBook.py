from bookLevel import lobLevel as level
from math import floor 
class orderBook:
    def __init__(self, instrumentName, tickSize):
        self.name = str(instrumentName)
        self.tickSize = float(tickSize)
        self.lob = {}
    
    def addLevel(self, ticks):
        tick = int(ticks)
        if not tick in  self.lob:
            self.lob[tick] = level(tick, self.tickSize)
    
    def sortLimitBook(self):
        if not self.lob.keys = sorted(self.lob):
            self.lob = {i:self.lob[i] for i in sorted(self.lob)}

    def postOrder(self, order):
        orderTicks = floor(order.price / self.tickSize)
        self.addLevel(orderTicks)
        self.lob[orderTicks].addOrder(order)

    def fillOrders(self, )
    
