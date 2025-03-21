from orderLevel import orderLevel as level
from order import Order as order

class orderBook:
    def __init__(self, instrumentID, tickSize):
        self.tickSize = float(tickSize)
        self.instrumentID = str(instrumentID)
        self.lob = {1:{}, 0:{}}
        self.mktOrders = {1:{}, 0:{}}
    
    def postOrder(self, order):
        rightInstrument = order.instrumentID == self.instrumentID
        if rightInstrument:
            isMarketOrder = order.type == 'mkt'
            order.price = round(order.price / self.tickSize) * self.tickSize
            if isMarketOrder:
                priceLevel = round(order.price / self.tickSize) * self.tickSize
                limitLevel = self.mktOrders[order.side]
                if not priceLevel in limitLevel:
                    limitLevel[priceLevel] = level(self.instrumentID, order.side, priceLevel)
                limitLevel[priceLevel].postOrder(order)
            else:
                priceLevel = round(order.price / self.tickSize) * self.tickSize
                limitLevel = self.lob[order.side]
                if not priceLevel in limitLevel:
                    limitLevel[priceLevel] = level(self.instrumentID, order.side, priceLevel)
                limitLevel[priceLevel].postOrder(order)

    @property
    def bestBidAsk(self):
        bidLevels = list(self.lob[1].keys())
        askLevels = list(self.lob[0].keys())
        bestBid = 'null' if len(bidLevels) == 0 else bidLevels[0]
        bestAsk = 'null' if len(askLevels) == 0 else askLevels[0]
        return bestBid, bestAsk
    
    @property
    def bestMarketLimits(self):
        bidLevels = list(self.mktOrders[1].keys())
        askLevels = list(self.mktOrders[0].keys())
        bestBid = 'null' if len(bidLevels) == 0 else bidLevels[0]
        bestAsk = 'null' if len(askLevels) == 0 else askLevels[0]
        return bestBid, bestAsk
    
    # TODO
    @property
    def aggressingMarketOrder(self):
        buySideAggressing, sellSideAggressing = False, False
        mktLimits = self.bestMarketLimits
        bbo = self.bestBidAsk
        
        # check market buy side for fillability
        if mktLimits[0] > bbo[1]:
            buySideAggressing = True
        if mktLimits[1] < bbo[0]:
            sellSideAggressing = True
        # TODO
        

    def fillOrder(self):
        pass

# TESTING:IGNORE
orders = orderBook('YLLSS', 5)
orders.postOrder(order('YLLSS', 1, 'Hairo', 'mkt', 100, -10, 1))
orders.postOrder(order('YLLSS', 3, 'Hairo', 'lim', 92, -10, 1))
orders.postOrder(order('YLLSS', 2, 'YCL', 'lim', 80, 10, 2))

#book = orders.mktOrders[1]
#print(book.side)
#print(book.type)
print(orders.bestBidAsk)
print(orders.bestMarketLimits)
book = orders.mktOrders[1]
#print(book)

                 
