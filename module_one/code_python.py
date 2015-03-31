import datetime
import sqlite3
import calendar
import pdb
import os

class sqlConnector:
	bSqlite3 = False
	bPostgre = True
	conn = 0
	portfolioDB = ''

	def __init__(self):
		#self.mnemo = mnemo
		if self.bSqlite3: 
			import sqlite3
			output = os.path.dirname(__file__)
			if not output: self.portfolioDB  = 'portfolio.db'
			else:
				self.portfolioDB = output + '/portfolio.db'
				output += "/"
			#conn = sqlite3.connect(portfolioDB)
			self.conn = sqlite3.connect(self.portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
			
		if self.bPostgre: 
			#import os
			import psycopg2
			import urlparse
			urlparse.uses_netloc.append("postgres")
			url = urlparse.urlparse(os.environ["DATABASE_URL"])
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

#print portfolioDB

def isWeekEnd(tDate):
        if tDate.weekday() == 5 or tDate.weekday() == 6: return True
	else:	return False

def isTradingDay(tDate):
	if isWeekEnd(tDate):
                return False
	else:	
		#conn = sqlite3.connect(portfolioDB)
		sqlConn = sqlConnector()
		c = sqlConn.conn.cursor()
		c.execute('SELECT COUNT(*) FROM calendar WHERE date = ?', (tDate.strftime("%Y-%m-%d"),))

		data = c.fetchone()[0]
		if data == 0:
			print('this is a trading day ' + tDate.isoformat())
			sqlConn.conn.close()			
			return True
		else:
			print('this is a HOLIDAY! ' + tDate.isoformat())
			sqlConn.conn.close()			
			return False

#q = datetime.datetime(2005,12,26)
#print isTradingDay(q)

def vTradingDates(stDate, endDate, cdr):
    #conn = sqlite3.connect(portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
	c.execute('SELECT * FROM calendar WHERE (CDR=?) AND (date BETWEEN ? AND ?)', (cdr, stDate, endDate))
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

def doRequestData(BBG, startD, endD):
	from datetime import date
	flag = 'close'
	if endD > date.today(): endD = date.today()
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
#	conn = sqlite3.connect(portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
	c = sqlConn.conn.cursor()
        tDate = vTradingDates(startD, endD, 'FR')
        c.execute('SELECT date FROM spots WHERE (date BETWEEN ? AND ?) AND (BBG=?) AND (flag=?)', (startD , endD, BBG, flag))
        oDate = [i[0] for i in c.fetchall()]

        mDate = list(set(tDate) - set(oDate))
        mDate.sort()
        print "missing Dates", mDate

        if mDate:
                mfile = open(output + "missingdates.csv", "w")
                convert_generator = (str(w)+';FR' for w in mDate)
                mfile.write('\n'.join(convert_generator))
                mfile.close()
                try: 
                        try: yahoo = Share(BBG)
                        except: print "yahoo = Share(?) failed... check your BBG or Internet Connection", BBG 
			
                        lDate = getDateforYahoo(mDate[0], mDate[-1])
                        print "ldate:", lDate, len(lDate)
                        
                        rslt = []
			#print lDate[0], lDate[-1]
			if lDate[0] == lDate[-1]:
				#print "here"
				#print yahoo.get_historical(lDate[0], lDate[-1])
				try: rslt.append(yahoo.get_historical(lDate[0], lDate[-1]))
                                except: print "yahoo request failed 1:", BBG, lDate[0], lDate[-1]
			else:
                        	for i in range(0,  len(lDate)-1):
                                	try: rslt = rslt + yahoo.get_historical(lDate[i], lDate[i+1])
                                	except: print "yahoo request failed 2:", BBG, lDate[i], lDate[i+1]
                        for line in rslt: 
                                if 'Close' in line: c.execute('INSERT INTO spots VALUES(?, ?, ?, ?)', (BBG, line['Date'], float(line['Close']), 'close'))
                                if 'Open' in line: c.execute('INSERT INTO spots VALUES(?, ?, ?, ?)', (BBG, line['Date'], float(line['Open']), 'open'))
                                if 'High' in line: c.execute('INSERT INTO spots VALUES(?, ?, ?, ?)', (BBG, line['Date'], float(line['High']), 'high'))
                                if 'Low' in line: c.execute('INSERT INTO spots VALUES(?, ?, ?, ?)', (BBG, line['Date'], float(line['Low']), 'low'))
                                if 'Volume' in line: c.execute('INSERT INTO spots VALUES(?, ?, ?, ?)', (BBG, line['Date'], float(line['Volume']), 'volume'))
                except: print "Ops!! your request failed!"
        sqlConn.conn.commit()
        sqlConn.conn.close()

def cTurbo(Fwd, strike, barrier, quot, margin):
	if Fwd > strike: return (Fwd - strike)/quot + margin
	else: 	return 0

def pTurbo(Fwd, strike, barrier, quot, margin):
	if strike > Fwd: return (strike - Fwd)/quot + margin
	else: 	return 0

class Stock(object):
        spot = 0.0
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
			#c = conn.cursor()
			try:
				c.execute("SELECT spot FROM spots WHERE BBG=? AND flag='close' AND date = (SELECT MAX(date) FROM spots WHERE BBG=? AND flag='close')", (self.mnemo, self.mnemo) )
				self.spot = c.fetchone()[0]
				try:
					sqlConn = sqlConnector()
					d = sqlConn.conn.cursor()
					#d = conn.cursor()
					d.execute("SELECT date, spot FROM spots WHERE BBG='" + self.mnemo + "' AND flag='close'" )
					self.spots =  dict(d.fetchall())
				except: print "error in loading historic prices for " + self.mnemo
			except: self.spot = 0
		self.loaded = True

	def saveQuote(self, dDate, quote):
		conn = sqlite3.connect(portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
		c = conn.cursor()
		try: 
			c.execute("INSERT INTO spot(BBG, date, spot, flag) VALUES(?,?,?,?)",(self.mnemo, dDate, quote, self.flag))
			c.commit()
		except: print "error in saving historic prices for " + self.mnemo

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
			#conn = sqlite3.connect(portfolioDB, detect_types=sqlite3.PARSE_DECLTYPES)
			sqlConn = sqlConnector()
			c = sqlConn.conn.cursor()
			#c = conn.cursor()
			c.execute('SELECT date, trans, BBG, qty, price, broker FROM trades WHERE (date BETWEEN ? AND ?)',(stDate, endDate))
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
        tDate = datetime.date(1999, 1, 5)
        #portfolio.trade(tDate, x, 1, x.getClose(tDate), 10)
        #portfolio.trade(tDate, x, 1, x.getClose(tDate), 10)
        portfolio.mDeposit(10000)
        #print "value at trade date:", portfolio.getValue(tDate,'close')
        #print "value as of today: ", portfolio.getValue(datetime.date(2014, 11, 26),'close')
        #print "gain: ", portfolio.getValue(datetime.date(2014, 11, 26),'close')-portfolio.getValue(tDate,'close')
        evalDate = datetime.date(2006, 1, 6)
        portfolio.load(datetime.date(2000, 01, 26), evalDate)
        print "portfolio values:", portfolio.getValue(evalDate,'close')
        print "total fees:", portfolio.getFees()

