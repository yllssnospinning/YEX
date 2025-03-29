class Order:
    def __init__(self, instrumentID, orderID, traderID, type, price, qty, priority):
        self.orderID = int(orderID)
        self.traderID = str(traderID)
        self.instrumentID = instrumentID

        self.base, self.quote = self.instrumentID.split('/')

        self.type = type
        self.price = float(price)

        self.side = 1 if qty > 0 else 0

        self.qty = abs(float(qty))
        self.prio = priority

        self.totCost = self.price * self.qty