from order import Order

class lobLevel:
    def __init__(self, tick, tickSize):
        self.bids, self.asks = [], []
        # Bids and Asks are stored in a list according to time priority
    
    def addOrder(self, appendOrder):
        # Order is a order class
        orderSturct = self.bids if appendOrder.direction == 1 else self.asks
        orderAppended = False
        for index, bookOrder in enumerate(orderSturct):
            if bookOrder.prio > appendOrder.prio:
                orderSturct.insert(index, appendOrder)
                orderAppended = True
                break
        if orderAppended == False:
            orderSturct.append(appendOrder)

    def fillOrders(self, side, quantity):
        orderSturct = self.bids if side == 1 else self.asks
        totalQty = float(quantity)
        for order in orderSturct:
            qtyToFill = min(order.qty, totalQty)
            if quantity > 0:
                order.qty = order.qty - qtyToFill
            totalQty -= qtyToFill
            print('Debug: Filled', order.traderID, qtyToFill, totalQty)
            if totalQty == 0:
                break

test = lobLevel(10, 1)
test.addOrder(Order(1, 'Hairo', 10, 10, 1))
test.addOrder(Order(2, 'Lychee', 10, 5, 1))
test.addOrder(Order(3, 'CYM', 10,  2, 1))
test.addOrder(Order(4, 'Bosco', 10, 0.5, 1))
print(test.bids)
print(test.asks)
test.fillOrders(1, 11)
