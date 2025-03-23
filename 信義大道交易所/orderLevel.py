class orderLevel:
    def __init__(self, instrumentID, side, price):
        try:
            self.price = float(price)
        except:
            self.price = price
        self.instrument = str(instrumentID)
        self.side = int(side)
        self.book = {}
        self.type = 'lim' if price != 'mkt' else 'mkt'

    def postOrder(self, order):
        orderPriority = order.prio
        rightInstrument = order.instrumentID == self.instrument
        rightPrice = order.price == self.price
        if self.type == 'mkt':
            rightPrice = True
        if rightInstrument and rightPrice:
            if orderPriority in self.book:
                self.book[orderPriority].append(order)
            else:
                #print('creating new prio level')
                self.book[orderPriority] = [order]
                # print(self.book)
                self.sortBook()
        else:
            print('cannot post order!')
    
    def sortBook(self):
        self.book = {i:self.book[i] for i in sorted(self.book.keys())}
    
    @property
    def levelRecentTimeQty(self):
        recentTime, totalQty = -1, 0
        for i in self.book:
            orders = self.book[i]
            for ii in orders:
                order = ii
                if recentTime == -1:
                    recentTime = order.orderID
                totalQty += abs(order.qty)
        
        return recentTime, totalQty
    
    def fillOrders(self, qty):
        amountToFill = float(qty)
        filledOrders = []
        for i in self.book:
            orders = self.book[i]
            for i, ii in enumerate(orders):
                if amountToFill == 0:
                    return []
                order = ii
                print(order.qty, amountToFill)
                orderFillQty = min(abs(order.qty), amountToFill)
                if order.qty > 0:
                    order.qty -= orderFillQty
                else:
                    order.qty += orderFillQty
                print(orderFillQty)
                if order.qty == 0:
                    orders.pop(i)
                amountToFill -= orderFillQty
                filledOrders.append([order.orderID, orderFillQty])
        return filledOrders