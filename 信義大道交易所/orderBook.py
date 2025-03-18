from orderLevel import orderLevel as level
from order import Order as order

class orderBook:
    def __init__(self, instrumentID, tickSize):
        self.tickSize = float(tickSize)
        self.instrumentID = str(instrumentID)
        self.lob = {1:{}, 0:{}}
        self.mktOrders = {1:level(self.instrumentID, 1, 'mkt'), 0:level(self.instrumentID, 0, 'mkt')}
    
    def postOrder(self, order):
        rightInstrument = order.instrumentID == self.instrumentID
        if rightInstrument:
            isMarketOrder = order.type == 'mkt'
            order.price = round(order.price / self.tickSize) * self.tickSize
            if isMarketOrder:
                #print('posting market order')
                self.mktOrders[order.side].postOrder(order)
            else:
                priceLevel = round(order.price / self.tickSize) * self.tickSize
                limitLevel = self.lob[order.side]
                if not priceLevel in limitLevel:
                    limitLevel[priceLevel] = level(self.instrumentID, order.side, priceLevel)
                limitLevel[priceLevel].postOrder(order)


orders = orderBook('YLLSS', 5)
orders.postOrder(order('YLLSS', 1, 'Hairo', 'mkt', 100, 10, 1))
orders.postOrder(order('YLLSS', 2, 'Hairo', 'lim', 92, 10, 1))

#book = orders.mktOrders[1]
#print(book.side)
#print(book.type)

book = orders.lob[1]


                 
