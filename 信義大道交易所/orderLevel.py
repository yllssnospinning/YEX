
class orderLevel:
    def __init__(self, instrumentID, side, price):
        self.price = float(price)
        self.instrument = str(instrument)
        self.side = int(side)
        self.book = {}

    def postOrder(self, order):
        orderPriority = order.prio
        rightInstrument = order.instrument == self.instrument
        rightPrice = order.price = self.price
        if rightInstrument and rightPrice:
            if orderPriority in self.book:
                self.book[orderPriority].append(order)
            else:
                self.book[orderPriority] = [order]
                self.sortBook()
    
    def sortBook(self):
        self.book = [self.book[i] for i in sorted(self.book.keys)]
    
    @property
    def levelRecentTimeQty(self):
        recentTime, totalQty = -1, 0
        for i in self.book:
            orders = self.book[i]
            for ii in orders:
                order = orders[ii]
                if recentTime == -1:
                    recentTime = order.orderID
                totalQty += abs(order.qty)
        
        return recentTime, totalQty
    
    def fillOrders(self, qty):
        amountToFill = float(qty)
        filledOrders = []
        for i in self.book:
            orders = self.book[i]
            for ii in orders:
                if amountToFill == 0:
                    return []
                order = orders[ii]
                orderFillQty = min(order.qty, amountToFill)
                order.qty -= orderFillQty
                amountToFill -= orderFillQty
                filledOrders.append([order.orderID, orderFillQty])
        return filledOrders
        
