from sqlconnector import *

class Stock(object):
	spot = 0.0
	lvolume = 0.0
	spots = {}
	mnemo = ""
	flag = "close"
	loaded = False
    
	def __init__(self, mnemo): self.mnemo = mnemo
	def load(self):
		if self.loaded == False:
			print "initializing new Stock... " + self.mnemo
#			sqlConn = sqlConnector()
			c = conn.cursor()
			try:
				c.execute("""SELECT "Close" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG = %s) AND BBG = %s)""", (self.mnemo, self.mnemo))
				self.spot = c.fetchone()[0]
				c.close()
				try:
#					sqlConn = sqlConnector()
					d = conn.cursor()
					d.execute("""SELECT "Date", "Close" FROM spots WHERE BBG=%s""", (self.mnemo, ))
					self.spots =  dict(d.fetchall())
					d.close()
					self.loaded = True
				except:
					print "error in loading historic prices for " + self.mnemo
			except:
				print "error in loading Stock!"
				self.spot = 0
    
	def load_numpy(self, stDate, endDate, flag):
		if self.loaded == False:
			print "loading Stock... " + self.mnemo, stDate, endDate, flag
			#try:
			if self.spot == 0:
				try:
#					sqlConn = sqlConnector()
					c = conn.cursor()
					c.execute("SELECT spot FROM spots WHERE (date=(SELECT MAX(date) FROM spots WHERE BBG = %s AND flag = 'close') AND BBG = %s AND flag = 'close')", (self.mnemo, self.mnemo))
					self.spot = c.fetchone()[0]
				except:
					print "error in loading Stock!"
			try:
				c.execute("SELECT date, spot FROM spots WHERE BBG=%s AND (date BETWEEN %s AND %s) AND flag=%s", (self.mnemo, stDate, endDate, flag))
				self.spots =  np.array(c.fetchall())
				self.loaded = True
			except:
				print "error in loading historic prices for " + self.mnemo
			c.close()
    
	def load_pandas(self, stDate, endDate, flag):
		import pandas as pds
		endDate = getLastTrDay(endDate)
		if self.loaded == False:
			print "loading Stock... " + self.mnemo, stDate, endDate, flag
			if self.spot == 0:
				try:
#					sqlConn = sqlConnector()
					resultss = pds.read_sql(("""SELECT "Close", "Volume" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG=%s) AND BBG = %s)"""), sqlConn.conn, params=(self.mnemo, self.mnemo))
					self.spot = resultss.iloc[0]['Close']
					self.lvolume = resultss.iloc[0]['Volume']
				except:
					print "error in loading Stock!"
			try:
				self.spots = pds.read_sql(("""SELECT "Date", "Close", "Volume" FROM spots WHERE BBG=%s AND ("Date" BETWEEN %s AND %s) ORDER BY "Date" ASC"""), sqlConn.conn, index_col="Date", params=(self.mnemo, stDate, endDate))
				self.spots['volume_20'] = pds.stats.moments.rolling_mean(self.spots['Volume'], 20)
				self.spots['ewma_10'] = pds.stats.moments.ewma(self.spots['Close'], 10)
				self.spots['ewma_20'] = pds.stats.moments.ewma(self.spots['Close'], 20)
				self.spots['ewma_50'] = pds.stats.moments.ewma(self.spots['Close'], 50)
				self.spots['ewma_100'] = pds.stats.moments.ewma(self.spots['Close'], 100)
				self.spots['var'] = self.spots[['Close','ewma_20','ewma_50','ewma_100']].var(axis=1)
				self.spots['mean'] = self.spots[['Close', 'ewma_20','ewma_50','ewma_100']].mean(axis=1)
				self.spots['cv'] = np.divide(np.sqrt(self.spots['var']),self.spots['mean'])
			except:
				print "error in loading historic prices for " + self.mnemo
			c.close()

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
		from pandas import DataFrame
		
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
		from pandas import DataFrame
		import pandas as pd
        
		toPlot = pd.DataFrame(self.spots[(self.spots.index > stDate)])
		df = DataFrame(toPlot[['Close', 'ewma_10', 'ewma_20', 'ewma_50', 'ewma_100']], index=toPlot.index)
		df.plot(title = self.mnemo);
		plt.show()

	def draw2(self, stDate, endDate):
		import math
		import pandas as pd
		import matplotlib.pyplot as plt
		
		toPlot = pd.DataFrame(self.spots[(self.spots.index > stDate)])
		print toPlot.tail()
		toPlot['Return'] = np.log(toPlot['Close'] / toPlot['Close']. shift( 1))
		toPlot['Mov_Vol'] = pd.rolling_std(toPlot['Return'], window = 20) * math.sqrt(252)
		toPlot[['Close', 'Mov_Vol', 'Return']].plot(subplots = True, style ='b', figsize =(8, 7), title = self.mnemo)
		plt.show()
    
	def trade(side, qty, price, fee,transDate):
#		sqlConn = sqlConnector()
		c = conn.cursor()
		try:
			c.execute("INSERT INTO trades(trans, bbg, qty, price, broker, date) VALUES(%s,%s,%s,%s,%s,%s)",(side, self.mnemo, qty, price, fee, transDate))
			c.commit()
		except: print "error in saving the trade in portfolio" + self.mnemo
		c.close()
