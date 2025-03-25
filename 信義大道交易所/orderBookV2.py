from limitDirectionalBook import limitBook as book

class orderBook:
    def __init__(self, instrumentName, tickSize):
        self.insName = str(instrumentName)
        self.tickSize = float(tickSize)
        self.limits = {1:book(self.insName, 1, 'lim', self.tickSize), 0:book(self.insName, 0, 'lim', self.tickSize)}
        self.mktStops = {1:book(self.insName, 1, 'mkt', self.tickSize), 0:book(self.insName, 0, 'mkt', self.tickSize)}
    
    def addOrder(self, order):
        rightInstrument = order.instrumentID == self.insName
        if order.type == 'lim':
            self.limits[order.side].postOrder(order)
        if order.type == 'mkt':
            self.mktStops[order.side].postOrder(order)
    
    @property
    def aggressingOrder(self):
        bidSidePriceTime = self.limits[1].bestPriceTime()
        askSidePriceTime = self.limits[0].bestPriceTime()
        mBidSidePriceTime = self.mktStops[1].bestPriceTime()
        mAskSidePriceTime = self.mktStops[0].bestPriceTime()
        mktBidAggressing, mktAskAggressing = False, False
        
        if mBidSidePriceTime[0] > askSidePriceTime[0]:
            mktBidAggressing = True
        if mAskSidePriceTime[0] < bidSidePriceTime[0]:
            mktAskAggressing = True
        if mktBidAggressing and mktAskAggressing:
            return 1, mBidSidePriceTime[2] if mBidSidePriceTime[1] < mAskSidePriceTime[1] else 0, mAskSidePriceTime[2]
        else:
            if mktBidAggressing:
                return 1, mBidSidePriceTime[2]
            if mktAskAggressing:
                return 0, mAskSidePriceTime[2]
            else:
                return -1, 'null'
        
        if bidSidePriceTime[0] < askSidePriceTime[0]:
            # There are no pair(s) of limit orders which can be filled
            return -1, 'allNull'
        # Bid side contains aggressing orders if its best order is placed earlier than that of the ask side, and vice versa
        if bidSidePriceTime[1] < askSidePriceTime[1]:
            return 1, bidSidePriceTime[2]
        else:
            return 0, askSidePriceTime[2]
    
    def matchOrders(self):
        matches = []
        while True:
            aggressingOrder = self.aggressingOrder
            if aggressingOrder[1].type == 'mkt':
                sideToMatch = 1 - aggressingOrder[0]
                orderToMatch = aggressingOrder[1]
                fills = self.limits[sideToMatch].fillOrders(incomingOrder=orderToMatch)
                matches.append([orderToMatch.orderID, fills])
            else:
                sideToMatch = 1 - aggressingOrder[0]
                orderToMatch = aggressingOrder[1]
                fills = self.limits[sideToMatch].fillOrders(incomingOrder=orderToMatch)
                matches.append([orderToMatch.orderID, fills])
            if aggressingOrder[1] == 'allNull':
                break
            