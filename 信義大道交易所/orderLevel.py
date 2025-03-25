from order import Order as order
class orderLevel:
    def __init__(self, instrumentID):
        self.instrument = str(instrumentID)
        self.book = {}

    def postOrder(self, order):
        orderPriority = order.prio
        rightInstrument = order.instrumentID == self.instrument
        if rightInstrument:
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
    
    def levelRecentTimeQty(self, timeOnly):
        # timeOnly = True
        recentTime, totalQty = -1, 0
        bestOrder = 'null'
        for i in self.book:
            orders = self.book[i]
            for ii in orders:
                order = ii
                print(order.qty)
                if recentTime == -1:
                    recentTime = order.orderID
                    bestOrder = order
                    if timeOnly:
                        return recentTime, bestOrder
                totalQty += abs(order.qty)
        return recentTime, totalQty, bestOrder

    def fillOrders(self, qty, incomingOrderName):
        amountToFill = qty
        filledOrders = []
        totalFilledQty = 0
        for prio in self.book:
            orders = self.book[prio]
            removedOrder = []
            for index, order in enumerate(orders):
                orderFillQty = min(order.qty, amountToFill)
                if order.traderID != incomingOrderName:
                    order.qty -= orderFillQty
                    totalFilledQty += orderFillQty
                    amountToFill -= orderFillQty
                    if order.qty == 0:
                        removedOrder.append(index)
                    filledOrders.append([order.orderID, orderFillQty])
                    if amountToFill == 0:
                        break
            # print(removedOrder)
            for i, ii in enumerate(removedOrder):
                orders.pop(ii - i)
        return filledOrders, totalFilledQty
