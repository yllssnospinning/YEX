from orderLevel import orderLevel as level

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
            if isMarketOrder:
                self.mktOrders[order.side].postOrder(order)
            else:
                priceLevel = round(order.price / self.tickSize) * self.tickSize
                limitLevel = self.lob[order.type]
                if not priceLevel in limitLevel:
                    limitLevel[priceLevel] = level(self.instrumentID, order.type, priceLevel)
                
