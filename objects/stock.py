
import common as cmn
import numpy as np
import pandas as pds

#import logging
#logging.basicConfig(level='ERROR', format='%(asctime)s - %(levelname)s - %(message)s')

import math
from common import *

class Stock(object):
    def __init__(self, mnemo):
        self.spot = 0.0
        self.lvolume = 0.0
        self.spots = pds.DataFrame()
        self.mnemo = mnemo
        flag = "close"
        self.loaded = False

#    def load(self):
#        if self.loaded == False:
#            print "initializing new Stock... " + self.mnemo
#            c = conn.cursor()
#            if True:
##            try:
#                c.execute("""SELECT "Close" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG = %s) AND BBG = %s)""", (self.mnemo, self.mnemo))
#                self.spot = c.fetchone()[0]
#                c.close()
#                if True:
##                try:
#                    d = conn.cursor()
#                    d.execute("""SELECT "Date", "Close" FROM spots WHERE BBG=%s""", (self.mnemo, ))
#                    self.spots =  dict(d.fetchall())
#                    d.close()
#                    self.loaded = True
##                except:
##                    print "error in loading historic prices for " + self.mnemo
##            except:
##                print "error in loading Stock!"
##                self.spot = 0
#
#    def load_numpy(self, stDate, endDate, flag):
#        if self.loaded == False:
#            print "loading Stock... " + self.mnemo, stDate, endDate, flag
#            if self.spot == 0:
#                if True:
##                try:
#                    c = conn.cursor()
#                    c.execute("SELECT spot FROM spots WHERE (date=(SELECT MAX(date) FROM spots WHERE BBG = %s AND flag = 'close') AND BBG = %s AND flag = 'close')", (self.mnemo, self.mnemo))
#                    self.spot = c.fetchone()[0]
##                except:
##                    print "error in loading Stock!"
#            if True:
##            try:
#                c.execute("SELECT date, spot FROM spots WHERE BBG=%s AND (date BETWEEN %s AND %s) AND flag=%s", (self.mnemo, stDate, endDate, flag))
#                self.spots =  np.array(c.fetchall())
#                self.loaded = True
##            if True:
##            except:
##                print "error in loading historic prices for " + self.mnemo
#            c.close()

    def load_pandas(self, stDate, endDate, flag):
        endDate = cmn.getLastTrDay(endDate)
        if self.loaded == False:
#            print "loading Stock... " + self.mnemo, stDate, endDate, flag
            logging.info('loading Stock... %s %s %s %s', self.mnemo, stDate, endDate, flag)
            if self.spot == 0:
                try:
                    resultss = pds.read_sql(("""SELECT "Close", "Volume" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG=%s) AND BBG = %s)"""), cmn.conn, params=(self.mnemo, self.mnemo))
                    self.spot = resultss.iloc[0]['Close']
                    self.lvolume = resultss.iloc[0]['Volume']
                except:
#                    print "error in loading Stock!"
                    logging.error('error in loading Stock!')
                    return False		
#            try:
            if True:
                self.spots = pds.read_sql(("""SELECT "Date", "Close", "Volume" FROM spots WHERE BBG=%s AND ("Date" BETWEEN %s AND %s) ORDER BY "Date" ASC"""), cmn.conn, index_col="Date", params=(self.mnemo, stDate, endDate))
                self.spots['volume_20'] = self.spots['Volume'].rolling(window=20,center=False).mean()
                self.spots['ewma_10'] = self.spots['Close'].ewm(ignore_na=False,min_periods=0,adjust=True,com=10).mean()
                self.spots['ewma_20'] = self.spots['Close'].ewm(ignore_na=False,min_periods=0,adjust=True,com=10).mean()
                self.spots['ewma_50'] = self.spots['Close'].ewm(ignore_na=False,min_periods=0,adjust=True,com=50).mean()
                self.spots['ewma_100'] = self.spots['Close'].ewm(ignore_na=False,min_periods=0,adjust=True,com=50).mean()
                
                self.spots['var'] = self.spots[['Close','ewma_20','ewma_50','ewma_100']].var(axis=1)
                self.spots['mean'] = self.spots[['Close', 'ewma_20','ewma_50','ewma_100']].mean(axis=1)
                self.spots['cv'] = np.divide(np.sqrt(self.spots['var']),self.spots['mean'])
                return True
#            except:
#                logging.error('error in loading historic prices for %s', self.mnemo)
#                return False                   

    def __hash__(self): return hash(str(self))
    def __cmp__(self, other): return cmp(str(self), str(other))
    def __str__(self): return self.mnemo
    def getMnemo(self): return self.mnemo
    def getClose(self, dDate):
        try : return self.spots[dDate]
        except : print "no close available for this stock at this date: "+ self.mnemo+" as of "+dDate.strftime("%Y-%m-%d")
        return 0
    def getSpot(self): return self.spot
    def setSpot(self, spot): self.spot = spot
    def draw(self, stDate, endDate):
        import matplotlib.pyplot as plt
        toPlot = self.spots[(self.spots.index > stDate)]
        lines = plt.plot(toPlot.index, toPlot['Close'])
        plt.plot(toPlot.index, toPlot['ewma_10'])
        plt.plot(toPlot.index, toPlot['ewma_20'])
        plt.plot(toPlot.index, toPlot['ewma_50'])
        plt.plot(toPlot.index, toPlot['ewma_100'])
        plt.setp(lines, 'color', 'r', 'linewidth', 2.0)
        plt.setp(plt.gca().get_xticklabels(), rotation = 30)
        plt.show()

    def draw3(self, stDate, endDate):
        import matplotlib.pyplot as plt
        toPlot = pds.DataFrame(self.spots[(self.spots.index > stDate)])
        df = pds.DataFrame(toPlot[['Close', 'ewma_10', 'ewma_20', 'ewma_50', 'ewma_100']], index=toPlot.index)
        df.plot(title = self.mnemo);
        plt.show()

    def draw2(self, stDate, endDate):
        import matplotlib.pyplot as plt
        toPlot = pds.DataFrame(self.spots[(self.spots.index > stDate)])
        print toPlot.tail()
        toPlot['Return'] = np.log(toPlot['Close'] / toPlot['Close']. shift( 1))
        toPlot['Mov_Vol'] = pds.rolling_std(toPlot['Return'], window = 20) * math.sqrt(252)
        toPlot[['Close', 'Mov_Vol', 'Return']].plot(subplots = True, style ='b', figsize =(8, 7), title = self.mnemo)
        plt.show()
    
    def trade(side, qty, price, fee,transDate):
        c = conn.cursor()
        try:
            c.execute("INSERT INTO trades(trans, bbg, qty, price, broker, date) VALUES(%s,%s,%s,%s,%s,%s)",(side, self.mnemo, qty, price, fee, transDate))
            c.commit()
        except: print "error in saving the trade in portfolio" + self.mnemo
        c.close()
