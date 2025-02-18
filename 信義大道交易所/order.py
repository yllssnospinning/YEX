class Order:
    def __init__(self, orderID, traderID, price, qty, priority):
        self.orderID = int(orderID)
        self.traderID = str(traderID)

        if price == 'mkt':
            self.type = 'mkt'
        else:
            self.type = 'lim'
            self.price = float(price)
        
        if qty > 0:
            self.direction = 1
        elif qty < 0:
            self.direction = 0
            
        self.qty = float(qty)
        self.prio = priority