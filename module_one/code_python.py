import datetime
import calendar
import pdb
import os
import numpy as np

from datetime import datetime

import pandas.io.data as web
import pandas.io.sql as pd
from sqlalchemy import create_engine
import pandas as pds

class sqlConnector:
	bPostgre = True
	conn = 0
	portfolioDB = ''
	output = ''
	engine = 0
	 #create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')

	def __init__(self):
		#if self.bSqlite3: 
		#	import sqlite3
		#	self.output = os.path.dirname(__file__)
		#	if not self.output: self.portfolioDB  = 'portfolio.db'
		#	else:
		#		self.portfolioDB = self.output + '/portfolio.db'
		#		self.output += "/"
		#	#conn = sqlite3.connect(portfolioDB)
		#	self.conn = sqlite3.connect(self.portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
		#if self.bPostgre: 
		import psycopg2
		import urlparse
		urlparse.uses_netloc.append("postgres")
		if not os.environ.has_key('DATABASE_URL'):
##			os.environ['DATABASE_URL'] = 'postgres://wcmikblybrgqbz:ZycOXg48gWJlRGR3MVFA9qGxvB@ec2-23-23-210-37.compute-1.amazonaws.com:5432/d3ibjjmjb9fqrm'
##			os.environ['DATABASE_URL'] = 'postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb'	
			os.environ['DATABASE_URL'] = 'postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb?sslca=config/ca/rds-ssl-ca-cert.pem&sslmode=require&encrypt=true'
			self.engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
##			os.environ['DATABASE_URL'] = 'postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb?sslca=rds-ssl-ca-cert.pem&sslmode=require&encrypt=true'
			#heroku config:add DATABASE_URL='postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb?sslca=config/ca/rds-ssl-ca-cert.pem&sslmode=require&encrypt=true'
		url = urlparse.urlparse(os.environ["DATABASE_URL"])
		#
		self.conn = psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)
		
calendar.setfirstweekday(calendar.MONDAY)

##########################################################
#import sys
#sys.path.append('~/module_yahoo/yahoo_finance')
from module_yahoo.yahoo_finance import Share
#from yahoo_finance import get_historical
#print "Share imported totototototo"
##########################################################

def isWeekEnd(tDate):
        if tDate.weekday() == 5 or tDate.weekday() == 6: return True
	else:	return False

def isTradingDay(tDate):
	if isWeekEnd(tDate):
                return False
	else:	
		sqlConn = sqlConnector()
		c = sqlConn.conn.cursor()
		c.execute('SELECT COUNT(*) FROM calendar WHERE date = %s', (tDate.strftime("%Y-%m-%d"),))
		data = c.fetchone()[0]
		if data == 0:
			print('this is a trading day ' + tDate.isoformat())
			sqlConn.conn.close()			
			return True
		else:
			print('this is a HOLIDAY! ' + tDate.isoformat())
			sqlConn.conn.close()			
			return False

def calendar_clean(theDates, CAL):
	theDates = theDates.to_datetime()
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
	holi = pds.read_sql("SELECT date FROM calendar WHERE (CDR=%s) AND (date BETWEEN %s AND %s) ORDER BY date ASC", sqlConn.conn, params=(CAL, theDates[0], theDates[-1]))
	holi = pds.to_datetime(holi['date'])
	return np.setdiff1d(theDates, holi)

def vTradingDates(stDate, endDate, cdr):
    #conn = sqlite3.connect(portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
	#if sqlConn.bSqlite3:	c.execute('SELECT * FROM calendar WHERE (CDR=?) AND (date BETWEEN ? AND ?)', (cdr, stDate, endDate))
	if sqlConn.bPostgre:	c.execute('SELECT * FROM calendar WHERE (CDR=%s) AND (date BETWEEN %s AND %s)', (cdr, stDate, endDate))	
	holidays = []
	for row in list(c): holidays.append(row[0])
	
	step = datetime.timedelta(days=1)
	result = []
	while stDate < endDate:
		if not isWeekEnd(stDate):                       
			if not stDate in holidays:
				result.append(stDate)
		stDate += step
	sqlConn.conn.close()
	return result

def getDateforYahoo(startD, endD):
        from datetime import timedelta
        result = [startD]
        for num in range(0, (endD - startD).days//365):
                result.append(result[-1] + timedelta(days=365))
        result.append(endD)        
        return result
		
def getLastTrDay(endD):
	from datetime import datetime
	from datetime import date
	import numpy as np
	import pandas as pds
	if endD >= date.today(): 
		if datetime.utcnow().hour > 8: lstTDR = np.busday_offset(date.today(), -1, roll='backward')
		else: lstTDR = np.busday_offset(endD, -2, roll='backward')
	lstTDR = pds.to_datetime(lstTDR)
	return lstTDR

"""def doRequestData(BBG, CAL, startD, endD):
	from datetime import date
	flag = 'close'
	if endD > date.today(): endD = date.today()
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
#	conn = sqlite3.connect(portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
	tDate = vTradingDates(startD, endD, CAL)
        
	#if sqlConn.bSqlite3: c.execute('SELECT date FROM spots WHERE (date BETWEEN ? AND ?) AND (BBG=?) AND (flag=?)', (startD , endD, BBG, flag))
	if sqlConn.bPostgre: c.execute('SELECT date FROM spots WHERE (date BETWEEN %s AND %s) AND (BBG=%s) AND (flag=%s)', (startD , endD, BBG, flag))
	oDate = [i[0] for i in c.fetchall()]
	
	mDate = list(set(tDate) - set(oDate))
	mDate.sort()
	print "missing Dates", mDate, " for: ", BBG 

	if mDate:
		mfile = open(sqlConn.output + "missingdates.csv", "w")
		convert_generator = (str(w)+';'+ CAL for w in mDate)
		mfile.write('\n'.join(convert_generator))
		mfile.close()
		try: 
			try: yahoo = Share(BBG)
			except: print "yahoo = Share(?) failed... check your BBG or Internet Connection", BBG 
			
			lDate = getDateforYahoo(mDate[0], mDate[-1])
			print "ldate:", lDate, len(lDate)
			rslt = []
			if lDate[0] == lDate[-1]:
				try: rslt.append(yahoo.get_historical(lDate[0], lDate[-1]))
				except: print "yahoo request failed 1:", BBG, lDate[0], lDate[-1]
			else:
				for i in range(0,  len(lDate)-1):
					try: rslt = rslt + yahoo.get_historical(lDate[i], lDate[i+1])
					except: print "yahoo request failed 2:", BBG, lDate[i], lDate[i+1]
			for line in rslt: 
				if 'Close' in line: c.execute('INSERT INTO spots VALUES(%s, %s, %s, %s)', (BBG, line['Date'], float(line['Close']), 'close'))
				if 'Open' in line: c.execute('INSERT INTO spots VALUES(%s, %s, %s, %s)', (BBG, line['Date'], float(line['Open']), 'open'))
				if 'High' in line: c.execute('INSERT INTO spots VALUES(%s, %s, %s, %s)', (BBG, line['Date'], float(line['High']), 'high'))
				if 'Low' in line: c.execute('INSERT INTO spots VALUES(%s, %s, %s, %s)', (BBG, line['Date'], float(line['Low']), 'low'))
				if 'Volume' in line: c.execute('INSERT INTO spots VALUES(%s, %s, %s, %s)', (BBG, line['Date'], float(line['Volume']), 'volume'))
		except: print "Ops!! your request failed!"
	sqlConn.conn.commit()
	sqlConn.conn.close()"""

def doRequestData(BBG, CAL, startD, endD):
	#flag = 'close'	
	from datetime import date
	endD = getLastTrDay(endD)
	print BBG, endD #.strftime("%Y-%m-%d")
#############################################################################################################################
	dates = calendar_clean(pds.date_range(start=startD, end=endD, freq ='1B'), CAL)
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
#############################################################################################################################	
	flag = 'Close'
	#fromdb = pds.read_sql("SELECT DISTINCT Date, %s FROM spots WHERE BBG=%s AND (Date BETWEEN %s AND %s) AND flag=%s ORDER BY Date ASC", sqlConn.conn, index_col='Date', params=(flag, BBG, startD, endD, flag), parse_dates=True)
	fromdb = pds.read_sql("""SELECT "Date", "Close" FROM spots WHERE BBG=%s AND ("Date" BETWEEN %s AND %s)""", sqlConn.conn, index_col="Date", params=(BBG, startD, endD), parse_dates=True)	
	#print "fromdb Date: ", fromdb.tail()
	toto = np.array(pds.to_datetime(fromdb.index))
	#print "toto: ", toto
	tempAlex = np.setdiff1d(dates, toto)
	#print "missing spots in DB for: ", BBG, tempAlex, len(tempAlex)
### optimisation du nombre de requete Yahoo #################################################################################
	toRequest = []
	if len(tempAlex) > 0:
		toRequest.append(pds.to_datetime(tempAlex[0]).date())
		for i in range(1, len(tempAlex)):
			#print i, tempAlex[i - 1], tempAlex[i], np.busday_count(pds.to_datetime(tempAlex[i - 1]).date(), pds.to_datetime(tempAlex[i]).date()), len(tempAlex)
			if i == len(tempAlex)-1: 
				toRequest.append(pds.to_datetime(tempAlex[i]).date())
			elif np.busday_count(pds.to_datetime(tempAlex[i - 1]).date(), pds.to_datetime(tempAlex[i]).date()) > 1:
				toRequest.append(pds.to_datetime(tempAlex[i]).date())
		toRequest.sort()
### save to DB ##############################################################################################################
		print "Period To Request for Stock: ", BBG, toRequest, len(toRequest)
		engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
		for row in range(1, len(toRequest)):
			fromyahoo = web.DataReader(name=BBG, data_source ='yahoo', start=toRequest[row-1], end=toRequest[row])
			fromyahoo['bbg'] = BBG
			fromyahoo.to_sql('spots', engine, if_exists='append') 

def cTurbo(Fwd, strike, barrier, quot, margin):
	if Fwd > strike: return (Fwd - strike)/quot + margin
	else: 	return 0

def pTurbo(Fwd, strike, barrier, quot, margin):
	if strike > Fwd: return (strike - Fwd)/quot + margin
	else: 	return 0

class Stock(object):
	spot = 0.0
	spots = 0
	#mavg30 = 0
	mnemo = ""
	flag = "close"
	loaded = False
        
	def __init__(self, mnemo): self.mnemo = mnemo
	def load(self):
		if self.loaded == False:
			print "initializing new Stock... " + self.mnemo
			#conn = sqlite3.connect(portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
			sqlConn = sqlConnector()
			c = sqlConn.conn.cursor()
			try:
#				c.execute("SELECT spot FROM spots WHERE (date=(SELECT MAX(date) FROM spots WHERE BBG = %s AND flag = 'close') AND BBG = %s AND flag = 'close')", (self.mnemo, self.mnemo))
				c.execute("""SELECT "Close" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG = %s) AND BBG = %s)""", (self.mnemo, self.mnemo))
				self.spot = c.fetchone()[0]
				sqlConn.conn.close()
				try:
					sqlConn = sqlConnector()
					d = sqlConn.conn.cursor()
					d.execute("""SELECT "Date", "Close" FROM spots WHERE BBG=%s""", (self.mnemo, ))
					self.spots =  dict(d.fetchall())
					sqlConn.conn.close()
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
					sqlConn = sqlConnector()
					c = sqlConn.conn.cursor()
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
			sqlConn.conn.close()

	def load_pandas(self, stDate, endDate, flag):
		#import pandas.io.sql as pds
		import pandas as pds
		if self.loaded == False:
			print "loading Stock... " + self.mnemo, stDate, endDate, flag
			if self.spot == 0:
				try:
					sqlConn = sqlConnector()
					c = sqlConn.conn.cursor()
					c.execute("""SELECT "Close" FROM spots WHERE ("Date"=(SELECT MAX("Date") FROM spots WHERE BBG=%s) AND BBG = %s)""", (self.mnemo, self.mnemo))
					self.spot = c.fetchone()[0]
				except:
					print "error in loading Stock!"
			try:
				#self.spots = pds.read_sql(("SELECT date, spot FROM spots WHERE BBG=%s AND (date BETWEEN %s AND %s) AND flag=%s ORDER BY date ASC"), sqlConn.conn, params=(self.mnemo, stDate, endDate, flag))				
				self.spots = pds.read_sql(("""SELECT "Date", "Close" FROM spots WHERE BBG=%s AND ("Date" BETWEEN %s AND %s) ORDER BY "Date" ASC"""), sqlConn.conn, params=(self.mnemo, stDate, endDate, flag))				
				self.spots['mavg_30'] = pds.stats.moments.rolling_mean(self.spots['Close'], 30)
				self.spots['ewma_10'] = pds.stats.moments.ewma(self.spots['Close'], 10)
				self.spots['ewma_20'] = pds.stats.moments.ewma(self.spots['Close'], 20)
				self.spots['ewma_50'] = pds.stats.moments.ewma(self.spots['Close'], 50)
				self.spots['ewma_100'] = pds.stats.moments.ewma(self.spots['Close'], 100)
				#self.spots['var'] = self.spots[['ewma_20','ewma_50','ewma_100']].var(axis=1)
				self.spots['var'] = self.spots[['Close','ewma_20','ewma_50','ewma_100']].var(axis=1)
				self.spots['mean'] = self.spots[['Close', 'ewma_20','ewma_50','ewma_100']].mean(axis=1)
				self.spots['cv'] = np.divide(np.sqrt(self.spots['var']),self.spots['mean'])
			except:
				print "error in loading historic prices for " + self.mnemo
			sqlConn.conn.close()
		
#	def saveQuote(self, dDate, quote):
#		sqlConn = sqlConnector()
#		c = sqlConn.conn.cursor()
#		try: 
#			c.execute("INSERT INTO spot(BBG, date, spot, flag) VALUES(%s,%s,%s,%s)",(self.mnemo, dDate, quote, self.flag))
#			c.commit()
#		except: print "error in saving historic prices for " + self.mnemo
#		sqlConn.conn.close()

	def __hash__(self): return hash(str(self))
	def __cmp__(self, other): return cmp(str(self), str(other))
	def __str__(self): return self.mnemo
	#def __eq__(self, other):
	#        #return (self.mnemo, self.location) == (other.mnemo, other.location)
	#        return (self.mnemo) == (other.mnemo)
	#def __ne__(self, other ):
	#	return self.mnemo != other.mnemo
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
		
		toPlot = self.spots[(self.spots.date > stDate)]		
		lines = plt.plot(toPlot['date'], toPlot['spot'])

		plt.plot(toPlot['date'], toPlot['ewma_10'])
		plt.plot(toPlot['date'], toPlot['ewma_20'])
		plt.plot(toPlot['date'], toPlot['ewma_50'])		
		plt.plot(toPlot['date'], toPlot['ewma_100'])		
		plt.setp(lines, 'color', 'r', 'linewidth', 2.0)

		plt.setp(plt.gca().get_xticklabels(), rotation = 30)
		
		plt.show()
		
	def draw2(self, stDate, endDate):
		import matplotlib.pyplot as plt 
		from pandas import DataFrame
		import pandas as pd
		
		toPlot = pd.DataFrame(self.spots[(self.spots.date > stDate)])
		toPlot.index = toPlot['date']

		df = DataFrame(toPlot[['spot', 'ewma_10', 'ewma_20', 'ewma_50', 'ewma_100']], index=toPlot.index)
		#plt.setp(plt.gca().get_xticklabels(), rotation = 30)
		#plt.figure(); 
		df.plot();
		plt.show()	
	def trade(side, qty, price, fee,transDate):
		sqlConn = sqlConnector()
		c = sqlConn.conn.cursor()
		try: 
			c.execute("INSERT INTO trades(trans, bbg, qty, price, broker, date) VALUES(%s,%s,%s,%s,%s,%s)",(side, self.mnemo, qty, price, fee, transDate))
			c.commit()
		except: print "error in saving the trade in portfolio" + self.mnemo
		sqlConn.conn.close()

class Portfolio:
        equity = {}
        cash = 0.0
        flag = 'close'
        fees = 0.0
        
	def __init__(self): self.cash = 0
	def mDeposit(self, amount): self.cash += amount
	def mWithdraw(self, amount): self.cash -= amount
	def getFees(self): return self.fees
	def trade(self, tDate, Stock, qt, price, fee):
		if Stock in self.equity: self.equity[Stock] = self.equity[Stock] + qt
		else : self.equity[Stock] = qt
                self.cash = self.cash - qt*price - fee
                self.fees += fee
	def getValue(self, gValue, flag):
		stockValue = 0.0
		for lStock, qty in self.equity.iteritems():
			stockValue += qty * lStock.getClose(gValue)
		return self.cash + stockValue 

	def load(self, stDate, endDate):
		sqlConn = sqlConnector()
		c = sqlConn.conn.cursor()
		from datetime import date
		if sqlConn.bPostgre: c.execute('SELECT date, trans, BBG, qty, price, broker FROM trades WHERE (date BETWEEN %s AND %s);', (stDate, endDate))
		holidays = []
		for row in c: 
			print row[0], row[1], row[2], row[3], row[4], row[5] 
			if row[1] == "BUY": self.trade(row[0], Stock(row[2]), row[3], row[4], row[5])
			elif row[1] == "SELL": self.trade(row[0], Stock(row[2]), -row[3], row[4], row[5])
			else: print "error in transaction side: ", row[1]
			toto = 0
			for lStock, qty in self.equity.iteritems():
				lStock.load()
				toto += 1
				print "toto:", toto
		sqlConn.conn.close		
	
if __name__=='__main__':
	import sys
#	try:	print int(sys.argv[1])
#	except: self = None
	dt = datetime.date(1990, 03, 01)
	end = datetime.date(2014, 12, 30)

	from timeit import Timer
	t = Timer(lambda: vTradingDates(dt, end, 'FR'))
	#print t.timeit(number=1)
	print t.repeat(3, 5)
	doRequestData('^FCHI', dt, end)
	#print vTradingDates(dt, end, 'FR')
	#print cTurbo(4346, 3750, 3750, 100.0, 0.08)
	#print pTurbo(4346, 4500, 4500, 100.0, 0.08)
	#x = Stock("^FCHI")
	#print x.spot
	#print x.getClose(datetime.date(1999, 1, 5))
	portfolio = Portfolio()
	#tDate = datetime.date(1999, 1, 5)
	#portfolio.trade(tDate, x, 1, x.getClose(tDate), 10)
	#portfolio.trade(tDate, x, 1, x.getClose(tDate), 10)
	portfolio.mDeposit(10000)
	#print "value at trade date:", portfolio.getValue(tDate,'close')
	#print "value as of today: ", portfolio.getValue(datetime.date(2014, 11, 26),'close')
	#print "gain: ", portfolio.getValue(datetime.date(2014, 11, 26),'close')-portfolio.getValue(tDate,'close')
	evalDate = datetime.date(2015, 04, 04)
	portfolio.load(datetime.date(2000, 01, 26), evalDate)
	print "portfolio values:", portfolio.getValue(evalDate,'close')
	print "total fees:", portfolio.getFees()

