class Order:
    def __init__(self, instrumentID, orderID, traderID, type, price, qty):
        self.orderID = int(orderID)
        self.traderID = str(traderID)
        self.instrumentID = instrumentID

        self.base, self.quote = self.instrumentID.split('/')

        self.type = type
        self.price = float(price)

        self.side = 'B' if qty > 0 else 'S'

        self.qty = abs(float(qty))

        self.totCost = self.price * self.qty
