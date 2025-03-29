from order import Order
class orderLevel:
    def __init__(self, instrumnetID, side):
        self.id, self.side = str(instrumentID), int(side)
        
    
    def addOrder(self, order):
        if order.instrumentID == self.id and order.side == self.side:
            