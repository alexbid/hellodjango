from sqlconnector import *
import stock
import datetime

class Portfolio:
    def __init__(self):
        self.cash = 0
        self.equity = {}
        self.flag = 'close'
        self.fees = 0.0
    
    def mDeposit(self, amount): self.cash += amount
    def mWithdraw(self, amount): self.cash -= amount
    def getFees(self): return self.fees
    def trade(self, tDate, Stock, qt, price, fee):
        if Stock in self.equity: self.equity[Stock] = self.equity[Stock] + qt
        else : self.equity[Stock] = qt
        self.cash = self.cash - qt*price - fee
        self.fees += fee
    def getValue(self, gValue, flag):
        #where gValue is evaluation date
        stockValue = 0.0
#        print self.equity
        for lStock, qty in self.equity.iteritems():
            stockValue += qty * lStock.getClose(gValue)
        return self.cash + stockValue
    
    def load(self, stDate, endDate):
        c = conn.cursor()
        c.execute('SELECT date, trans, BBG, qty, price, broker FROM trades WHERE (date BETWEEN %s AND %s);', (stDate, endDate))
        holidays = []
        for row in c:
            print row[0], row[1], row[2], row[3], row[4], row[5]
            if row[1] == "BUY": self.trade(row[0], stock.Stock(row[2]), row[3], row[4], row[5])
            elif row[1] == "SELL": self.trade(row[0], stock.Stock(row[2]), -row[3], row[4], row[5])
            else: print "error in transaction side: ", row[1]
            toto = 0
            for lStock, qty in self.equity.iteritems():
                lStock.load()
                toto += 1
                print "toto:", toto
        c.close()

if __name__=='__main__':
    
    stDate = datetime.date(1990, 03, 01)
    endDate = datetime.date(2015, 12, 30)
    
    p = Portfolio()
    p.load(stDate, endDate)
    p.getValue(stDate, 'close')
