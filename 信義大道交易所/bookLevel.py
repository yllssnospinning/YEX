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
            qtyToFill = min(order.qty, quantity)
            if quantity > 0:
                order.qty = order.qty - qtyToFill
    