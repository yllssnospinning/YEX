from orderLevel import orderLevel
class sideBook:
    def __init__(self, instrumentID, side):
        self.instrumentID = str(instrumentID)
        self.side = int(side)
        self.book = {}
    
    def postOrder(self, order):
        if order.instrumentID == self.instrumentID and order.side = self.side:
            if not order.price in self.book:
                self.book[order.price] = orderLevel(self.instrumentID, self.side)
            self.book[order.price].postOrder(order)
            
    def sortBook(self):
        self.book = {i:self.book[i]}       
    
    def fillOrders(self, incomingOrder):
        for i in 