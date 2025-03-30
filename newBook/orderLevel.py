from order import Order
class orderLevel:
    def __init__(self, instrumentID, side):
        self.id, self.side = str(instrumentID), int(side)
        self.orders = []
        self.removedOrders = []
    
    def postOrder(self, order):
        if order.instrumentID == self.id and order.side == self.side:
            if order.prio == 0:
                self.orders.append(order)
            if order.prio == 1:
                self.orders.insert(0, order)
    @property
    def bestTime(self):
        return self.orders[0] if len(self.orders) > 0 else 'null'
    
    def fillOrders(self, incomingOrder):
        orderToFill = incomingOrder
        qtyToFill = incomingOrder.qty
        totalQuantityFilled = 0
        ordersToRemove = []
        for i, order in enumerate(self.orders):
            incomingBuy = incomingOrder.side == 1
            orderRemoved = order.orderID in self.removedOrders
            if orderRemoved:
                ordersToRemove.append(i)
            else:
                priceFufilled = order.price < incomingOrder.price if incomingBuy else order.price > incomingOrder.price
                if priceFufilled:
                    pairFillQty = min(incomingOrder.qty, order.qty)
                    order.qty -= pairFillQty
                    orderToFill.qty -= pairFillQty
                    totalQuantityFilled += pairFillQty
                    if order.qty == 0:
                        ordersToRemove.append(i)
        for i, ii in enumerate(ordersToRemove):
            self.orders.pop(ii - i)
        return totalQuantityFilled
    