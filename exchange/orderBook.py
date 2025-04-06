from sideBook import sideBook

class orderBook(self):
    def __init__(self, instrumentName, tickSize):
        self.mBuy = sideBook('mktStop', 1)
        self.mSell = sideBook('mktStop', 0)
        self.lBuy = sideBook('lim', 1)
        self.lSell = sideBook('lim', 0)
        
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