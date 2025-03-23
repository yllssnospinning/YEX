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
        bbTimeQty, baTimeQty = 'null', 'null'
        if not bestBid == 'null':
            bbTimeQty = self.lob[1][bestBid].levelRecentTimeQty            
        if not bestAsk == 'null':
            baTimeQty = self.lob[0][bestAsk].levelRecentTimeQty
        return bestBid, bestAsk, bbTimeQty, baTimeQty
    
    @property
    def bestMarketLimits(self):
        bidLevels = list(self.mktOrders[1].keys())
        askLevels = list(self.mktOrders[0].keys())
        bestBid = 'null' if len(bidLevels) == 0 else bidLevels[0]
        bestAsk = 'null' if len(askLevels) == 0 else askLevels[0]
        bbTimeQty, baTimeQty = 'null', 'null'
        if not bestBid == 'null':
            bbTimeQty = self.mktOrders[1][bestBid].levelRecentTimeQty            
        if not bestAsk == 'null':
            baTimeQty = self.mktOrders[0][bestAsk].levelRecentTimeQty
        return bestBid, bestAsk, bbTimeQty, baTimeQty
    # TODO
    
    @property
    def aggressingMarketOrder(self):
        buySideAggressing, sellSideAggressing = False, False
        mktLimits = self.bestMarketLimits
        bbo = self.bestBidAsk
        # check market buy side for fillability
        if not mktLimits[0] == 'null':
            if mktLimits[0] >= bbo[1]:
                buySideAggressing = True
        if not mktLimits[1] == 'null':
            if mktLimits[1] <= bbo[0]:
                sellSideAggressing = True
        if buySideAggressing and sellSideAggressing:
            if mktLimits[2][0] < mktLimits[3][0]:
                sellSideAggressing = False
            else:
                buySideAggressing = False
        if buySideAggressing:
            return 1
        elif sellSideAggressing:
            return 0
        else:
            return -1
        
    @property
    def aggressingLimitOrder(self):
        buySideAggressing, sellSideAggressing = False, False
        bbo = self.bestBidAsk
        if bbo[0] == 'null' and bbo[1] == 'null':
            return -1
        else:
            if bbo[0] < bbo[1]:
                return -1
            elif bbo[1] == 'null':
                return 1
            elif bbo[0] == 'null':
                return 0
            else:
                buySideAggressing = bbo[2][0] < bbo[3][0]
                return 1 if buySideAggressing else 0

    def fillOrder(self):
        while True:
            mktAggressing = self.aggressingMarketOrder
            if mktAggressing != -1:
                limitSideToMatch = 1 - mktAggressing
                


# TESTING:IGNORE
orders = orderBook('YLLSS', 5)
orders.postOrder(order('YLLSS', 1, 'Hairo', 'mkt', 100, 10, 1))
orders.postOrder(order('YLLSS', 2, 'Lychee', 'mkt', 100, -30, 2))
orders.postOrder(order('YLLSS', 3, 'Hairo', 'lim', 100, -100, 1))
orders.postOrder(order('YLLSS', 4, 'YCL', 'lim', 80, 10, 2))
orders.postOrder(order('YLLSS', 5, 'Hairo', 'lim', 70, -100, 2))
orders.postOrder(order('YLLSS', 6, 'YCL', 'lim', 72, -10, 1))

#book = orders.mktOrders[1]
#print(book.side)
#print(book.type)
print(orders.bestBidAsk)
print(orders.bestMarketLimits)
print(orders.aggressingMarketOrder)
print(orders.aggressingLimitOrder)
book = orders.mktOrders[1]
#print(book)