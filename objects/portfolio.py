from sqlconnector import *
import stock
import datetime
from common import *
from dateutil.relativedelta import relativedelta
import numpy as np

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
    def getValue(self, evalDate, flag):
        #where evalDate is evaluation date
        stockValue = 0.0
        for lStock, qty in self.equity.iteritems():
            stockValue += qty * lStock.getClose(evalDate)
        return self.cash + stockValue
    
    # def getPosition(self, evalDate):
    #     #where evalDate is evaluation date
    #     stockValue = 0.0
    #     for lStock, qty in self.equity.iteritems():
    #         stockValue += qty * lStock.getClose(evalDate)
    #     return self.cash + stockValue

    def load(self, stDate, endDate):
        c = conn.cursor()
        c.execute('SELECT date, trans, BBG, qty, price, broker FROM trades WHERE (date BETWEEN %s AND %s);', (stDate, endDate))
        holidays = []
        for row in c:
            logging.info('loading Trades... %s %s %s %s %s %s', row[0], row[1], row[2], row[3], row[4], row[5])
            if row[1] == "BUY": self.trade(row[0], stock.Stock(row[2]), row[3], row[4], row[5])
            elif row[1] == "SELL": self.trade(row[0], stock.Stock(row[2]), -row[3], row[4], row[5])
            else: print "error in transaction side: ", row[1]
            toto = 0
            for lStock, qty in self.equity.iteritems():
                lStock.load_pandas(stDate, endDate, "close")
                toto += 1
        c.close()

    def getVAR_Histo(self, evalDate):
        stDate = evalDate + relativedelta(months=-12)

        # get market data
        self.spots = pds.read_sql(("""SELECT DISTINCT "Date", "Close", "bbg" FROM spots WHERE ("Date" BETWEEN %s AND %s) ORDER BY "Date" ASC"""), conn, columns="bbg", index_col="Date", params=(stDate, evalDate))
        
        result = pds.DataFrame()
        result.index.name = "Date"

        for item in self.spots["bbg"].unique():
            df5 = pds.DataFrame(self.spots[self.spots["bbg"] == item]["Close"])
            df5.columns = [item]
            result =  pds.merge(result, df5,  left_index=True, right_index=True, how='outer')

        price = result[~result.index.duplicated(keep='first')]
        returns = price.pct_change(1).fillna(value=0)
        rt = returns.as_matrix(columns=list(self.equity.keys()))
        rt += 1

        # get positions
        buff = []
        for lStock, qty in self.equity.iteritems(): buff.append(qty * lStock.getClose(evalDate))
        x = np.array(buff)

        pl = np.sum(np.transpose(x) * rt, axis=1)
        return np.percentile(pl, 1) - np.sum(x)

if __name__=='__main__':
    
    stDate = datetime.date(1990, 03, 01)
    endDate = datetime.date(2017, 12, 30)
    
    p = Portfolio()
    p.mDeposit(1000)
    p.load(stDate, endDate)
    print p.getValue(endDate, 'close')
    print 'VAR Histo:', p.getVAR_Histo(endDate)






