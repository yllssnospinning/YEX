from sideBook import sideBook

class orderBook(self):
    def __init__(self, instrumentName, tickSize):
        self.mBuy = sideBook('mktStop', 1)
        self.mSell = sideBook('mktStop', 0)
        self.lBuy = sideBook('lim', 1)
        self.lSell = sideBook('lim', 0)
        
    def addOrder(self, order):
        if order.side = 'B':
            if order.type = 'mktStop':
                self.mBuy.append(order)
            else:
                self.lBuy.append(order)
        else:
            if order.type = 'mktStop':
                self.mBuy.append(order)
            else:
                self.lBuy.append(order)
        
    def getAggressingOrder(self):
        mktBuyAggressing, mktSellAggressing = True, True
        bestMktBuy = self.mBuy.bestOrder
        bestMktSell = self.mSell.bestOrder
        bestLimBuy = self.lBuy.bestOrder
        bestLimSell = self.lSell.bestOrder
        if not bestMktBuy is None and bestMktSell is None:
            if bestLimSell is None:
                mktBuyAggressing = False
            elif bestLimSell.price > bestMktBuy.price:
                mktBuyAggressing = False
            if bestLimBuy is None:
                mktSellAggressing = False
            elif bestLimBuy.price < bestMktSell.price:
                mktSellAggressing = False
        if not mktBuyAggressing == False and mktSellAggressing == False:
            if mktBuyAggressing and mktSellAggressing:
                return bestMktBuy if bestMktBuy.orderID < bestMktSell.orderID else bestMktSell
            elif mktBuyAggressing:
                return mktBuyAggressing
            else:
                return mktSellAggressing
        
        if bestLimBuy.price > bestLimSell.price:
            return bestLimBuy if bestLimBuy.orderID < bestLimSell.orderID else bestLimSell

    def fillOrders(self):
        totalFills = []
        while True:
            aggressingOrder = self.getAggressingOrder()
            if aggressingOrder is None:
                break
            fills = []
            if aggressingOrder.side = 'B':
                fills = self.lSell.fillOrders(incomingOrder=aggressingOrder)
            else:
                fills = self.lBuy.fillOrders(incomingOrder=aggressingOrder)
            totalFills.extend(fills)
            
            