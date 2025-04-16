class account:
    def __init__(self):
        self.assets = {}
        self.openOrders = {}
    
    def getOutstandingOrderValue(self, valueToAssess):
        totalValue = 0
        for pairTicker in self.openOrders:
            sell, buy = pairTicker.split()
            assessmentSide = 0
            if buy == valueToAssess:
                assessmentSide = 'B'
            elif sell == valueToAssess:
                assessmentSide = 'S'
            if assessmentSide != 0:
                orders = self.openOrders[pairTicker]
            
            