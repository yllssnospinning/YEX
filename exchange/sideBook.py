class sideBook:
    def __init__(self, orderType, orderSide):
        self.type = str(orderType), str(orderSide)
        self.book = {}
    
    def postOrder(self, order):
        if not order.price in self.book:
            self.book[order.price] = [order]
        else:
            self.book[order.price].append(order)

    def fillBestOrder(self, qty):
        try:
            priceLevels = list(self.book.keys())
            bestLevel = self.book[priceLevels[0]]
            bestOrder = bestLevel[0]
            bestOrder.qty -= qty
            if bestOrder.qty <= 0:
                bestLevel.pop(0)
                if len(bestLevel) == 0:
                    del bestLevel[priceLevels[0]]
        except:
            return None
            
    def bestOrder(self, traderID):
        priceLevels = list(self.book.keys())
        if len(priceLevels) == 0:
            return None
        else:
            for price in self.book:
                level = self.book[price]
                for order in level:
                    if not order.traderID == traderID:
                        return order
                    
    def fillOrders(self, incomingOrder):
        inc = incomingOrder
        totalFillQty = 0
        totalFillAmount = 0
        fills = []
        lastBestPrice, canFill = 0, False
        while True:
            priceLevels = list(self.book.keys())
            bestPrice = priceLevels[0] if len(priceLevels) > 0 else 'null'
            if not lastBestPrice == bestPrice:
                print(incomingOrder.price, bestPrice)
                if bestPrice == 'null':
                    break
                canFill = incomingOrder.side == 'B' and bestPrice < incomingOrder.price or incomingOrder.side == 'S' and bestPrice > incomingOrder.price
            if inc.qty == 0:
                canFill = False 
            if canFill:
                priceLevel = self.book[bestPrice]
                orderToFill = priceLevel[0]
                maxFillQty = min(orderToFill.qty, inc.qty)
                orderToFill.qty -= maxFillQty
                inc.qty -= maxFillQty
                totalFillQty += maxFillQty
                fillPrice = 0
                if incomingOrder.type == 'mktStop':
                    fillPrice = orderToFill.price
                else:
                    fillPrice = incomingOrder.price if incomingOrder.orderID < orderToFill.orderID else orderToFill.price
                totalFillAmount += maxFillQty * fillPrice
                fills.append([orderToFill.orderID, fillPrice, maxFillQty])
                if orderToFill.qty == 0:
                    priceLevel.pop(0)
                    if len(priceLevel) == 0:
                        del self.book[bestPrice]
            else:
                break
        incomingOrderFill = []
        if totalFillQty != 0:
            incomingOrderFill = [incomingOrder.orderID, totalFillAmount / totalFillQty, totalFillQty]
        return fills, incomingOrderFill
             