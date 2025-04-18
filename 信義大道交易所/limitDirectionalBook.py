from orderLevel import orderLevel as level
from order import Order as order

class limitBook:
    def __init__(self, instrumentName, side, type, tickSize):
        self.insName = str(instrumentName)
        self.side = int(side)
        self.type = str(type)
        self.tickSize = float(tickSize)
        self.book = {}
    
    def convertPriceLevel(self, price):
        if price % self.tickSize != 0:
            newPrice = round(price / self.tickSize) * self.tickSize
            return newPrice
        else:
            return price
    
    def postOrder(self, order):
        rightInstrument = order.instrumentID == self.insName
        rightSide = order.side == self.side
        rightType = order.type == self.type
        if rightInstrument and rightSide and rightType:
            order.price = self.convertPriceLevel(order.price)
            if order.price in self.book:
                self.book[order.price].postOrder(order)
            else:
                self.book[order.price] = level(self.insName)
                self.book[order.price].postOrder(order)
                self.sortBook()
                
    def fillOrders(self, incomingOrder):
        order = incomingOrder
        qtyToFill = incomingOrder.qty
        totalFilledQty = 0
        fills = {}
        for priceLevel in self.book:
            print(priceLevel, incomingOrder.price, incomingOrder.type)
            if incomingOrder.side == 1 and priceLevel > incomingOrder.price or incomingOrder.side == 0 and priceLevel < incomingOrder.price:
                break
            fill = self.book[priceLevel].fillOrders(qtyToFill, order.traderID)
            fills[priceLevel] = fill[0]
            totalFilledQty += fill[1]
            qtyToFill -= fill[1]
        return fills, totalFilledQty

    
    def sortBook(self):
        self.book = {i:self.book[i] for i in sorted(list(self.book.keys()), reverse=self.side == 1)}
        
    def bestPriceTime(self):
        try:
            bestPrice = list(self.book.keys())[0]
        except:
            return 'null'
        bpLevel = self.book[bestPrice]
        time = bpLevel.levelRecentTimeQty(True)
        return bestPrice, time[0], time[1] 
    
# TODO: Remove orderLevel if all orders in it are filled    
def testBook():
    book = limitBook('HairoCoin', 1, 'lim', 5)
    book.postOrder(order('HairoCoin', 1, 'Hairo', 'lim', 100, 20, 1))
    book.postOrder(order('HairoCoin', 2, 'YCL', 'lim', 100, 90, 0))
    book.postOrder(order('HairoCoin', 3, 'Chlochlonut', 'lim', 100, 10, 1))
    book.postOrder(order('HairoCoin', 4, 'Miss_LBL', 'lim', 80, 90, 2))
    incoming = order('HairoCoin', 3, 'Lychee', 'lim', 80, -125, 0)
    #print(incoming.side)
    print(book.fillOrders(incoming))
    #print(book.book[80].levelRecentTimeQty(False))
#print(book.bestPriceTime)
testBook()

