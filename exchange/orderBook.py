from sideBook import sideBook
from order import Order

class orderBook:
    def __init__(self, instrumentName, tickSize):
        self.mBuy = sideBook('mktStop', 1)
        self.mSell = sideBook('mktStop', 0)
        self.lBuy = sideBook('lim', 1)
        self.lSell = sideBook('lim', 0)
        
    def addOrder(self, order):
        if order.side == 'B':
            if order.type == 'mktStop':
                self.mBuy.postOrder(order)
            else:
                self.lBuy.postOrder(order)
        else:
            if order.type == 'mktStop':
                self.mSell.postOrder(order)
            else:
                self.lSell.postOrder(order)
        
    def getAggressingOrder(self):
        mktBuyAggressing, mktSellAggressing = False, False
        bestMktBuy = self.mBuy.bestOrder(traderID = None)
        if bestMktBuy is not None:
            match = self.lSell.bestOrder(traderID = bestMktBuy.traderID)
            if match is not None and match.price < bestMktBuy.price:
                mktBuyAggressing = True
        bestMktSell = self.mSell.bestOrder(traderID = 'null')
        if bestMktSell is not None:
            match = self.lBuy.bestOrder(traderID = bestMktSell.traderID)
            if match is not None and match.price > bestMktSell.price:
                mktSellAggressing = True
        if mktBuyAggressing and mktSellAggressing:
            return bestMktBuy if bestMktBuy.orderID < bestMktSell.orderID else bestMktSell
        if mktBuyAggressing:
            return bestMktBuy
        if mktSellAggressing:
            return bestMktSell
        
        limBuyAggressing, limSellAggressing = False, False
        bestLimBuy = self.lBuy.bestOrder(traderID = None)
        if not bestLimBuy is None:
            match = self.lBuy.bestOrder(traderID = bestLimBuy.traderID)
            if match is not None and match.price < bestLimBuy.price:
                limBuyAggressing = True
        bestLimSell = self.lSell.bestOrder(traderID = None)
        if not bestLimSell is None:
            match = self.lSell.bestOrder(traderID = bestLimSell.traderID)
            if match is not None and match.price > bestLimSell.price:
                limSellAggressing = True
        if limBuyAggressing and limSellAggressing:
            return bestLimBuy if bestLimBuy.orderID < bestLimSell.orderID else bestLimSell
        if limBuyAggressing:
            return bestLimBuy
        if limSellAggressing:
            return bestLimSell
    
    
    def fillOrders(self):
        totalFills = []
        while True:
            aggressingOrder = self.getAggressingOrder()
            if aggressingOrder is None:
                break
            print(aggressingOrder.side, aggressingOrder.type, aggressingOrder.price, aggressingOrder.qty)
            fills = []
            if aggressingOrder.side == 'B':
                fills = self.lSell.fillOrders(incomingOrder=aggressingOrder)
                print('fill Buy')
                if aggressingOrder.type == 'lim':
                    self.lBuy.fillBestOrder(qty=fills[1][2])
                else:
                    self.mBuy.fillBestOrder(qty=fills[1][2])
            else:
                print('fill Sell')
                fills = self.lBuy.fillOrders(incomingOrder=aggressingOrder)
                if aggressingOrder.type == 'lim':
                    self.lSell.fillBestOrder(qty=fills[1][2])
                else:
                    self.mSell.fillBestOrder(qty=fills[1][2])
            #print(fills)
            totalFills.extend(fills)
        return totalFills
            

book = orderBook('HAIRO/YNT', 1)
book.addOrder(Order(instrumentID='HAIRO/YNT', orderID=1, traderID='Hairo', type='lim', price=100,qty=10))
book.addOrder(Order(instrumentID='HAIRO/YNT', orderID=2, traderID='Tikey', type='lim', price=99, qty=15))
book.addOrder(Order(instrumentID='HAIRO/YNT', orderID=3, traderID='Lychee', type='lim', price=99, qty=2))
book.addOrder(Order(instrumentID='HAIRO/YNT', orderID=5, traderID='Bosco', type='lim', price=75, qty=-5))
book.addOrder(Order(instrumentID='HAIRO/YNT', orderID=4, traderID='Bosco', type='lim', price=80, qty=-16))
print(book.fillOrders())
#book.mSell.fillBestOrder(16)
#print(book.lBuy.fillOrders(Order(instrumentID='HAIRO/YNT', orderID=4, traderID='Bosco', type='mktStop', price=12, qty=-16)))
print(book.mSell.book)