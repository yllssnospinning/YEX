
class account:
    def __init__(self, accountName):
        self.assets = {}
        self.openOrders = {}
    
    def openOrder(self, order):
        instrumentID = order.instrumentID
        if not instrumentID in self.openOrders:
            self.openOrders[instrumentID] = []
        self.openOrders.append(order)
        
    @property    
    def totalOrdersMaxCost(self):
        totValue = {}
        for insturment in self.openOrders:
            for order in self.openOrders[insturment]:
                if order.type == 1: #we only look at bids here
                    assetOut = order.quote
                    if not assetOut in totValue:
                        totValue[assetOut] = 0
                    totValue[assetOut] += order.totCost
        return totValue

    def getBuyingPower(self):
        buyingPwr = {}
        outstandingOrders = self.get