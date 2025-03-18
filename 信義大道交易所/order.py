class Order:
    def __init__(self, instrumentID, orderID, traderID, type, price, qty, priority):
        self.orderID = int(orderID)
        self.traderID = str(traderID)
        self.instrumentID = instrumentID

        self.type = type
        self.price = float(price)

        self.side = 1 if qty > 0 else 0

        self.qty = float(qty)
        self.prio = priority

