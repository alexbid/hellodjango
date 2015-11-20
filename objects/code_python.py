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
	theDates = np.array(theDates.to_datetime())
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
	holi = pds.read_sql("SELECT date FROM calendar WHERE (CDR=%s) AND (date BETWEEN %s AND %s) ORDER BY date ASC", sqlConn.conn, index_col='date', params=(CAL, pd.to_datetime(theDates[0]).strftime('%Y-%m-%d'), pd.to_datetime(theDates[-1]).strftime('%Y-%m-%d')))
	holi = np.array(pds.to_datetime(holi.index))
	return np.setdiff1d(theDates, holi)

def vTradingDates(stDate, endDate, cdr):
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
	c.execute('SELECT * FROM calendar WHERE (CDR=%s) AND (date BETWEEN %s AND %s)', (cdr, stDate, endDate))	
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
	refDate = datetime.date(datetime.utcnow())
	refHour = datetime.utcnow().hour
	print refDate
	#if endD >= date.today(): 
	if endD >= refDate: 
		#print "hour: ", datetime.utcnow().hour, np.busday_offset(date.today(), 0, roll='backward'), np.is_busday(date.today())
		if np.is_busday(refDate):
			if refHour > 6: lstTDR = np.busday_offset(refDate, -1, roll='backward')
			else: lstTDR = np.busday_offset(endD, -2, roll='backward')
		else:
			if refHour > 6: lstTDR = np.busday_offset(refDate, 0, roll='backward')
			else: lstTDR = np.busday_offset(endD, -2, roll='backward')
	buff = pds.to_datetime(lstTDR)
	return buff

def doRequestData(BBG, CAL, startD, endD):
	from datetime import date
	endD = getLastTrDay(endD)
	print BBG, endD
#############################################################################################################################
	dates = calendar_clean(pds.date_range(start=startD, end=endD, freq ='1B').to_datetime(), CAL)
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
#############################################################################################################################	
	flag = 'Close'
	#fromdb = pds.read_sql("SELECT DISTINCT Date, %s FROM spots WHERE BBG=%s AND (Date BETWEEN %s AND %s) AND flag=%s ORDER BY Date ASC", sqlConn.conn, index_col='Date', params=(flag, BBG, startD, endD, flag), parse_dates=True)
	fromdb = pds.read_sql("""SELECT "Date", "Close" FROM spots WHERE BBG=%s AND ("Date" BETWEEN %s AND %s)""", sqlConn.conn, index_col="Date", params=(BBG, startD, endD), parse_dates=True)	
	toto = np.array(pds.to_datetime(fromdb.index))
	tempAlex = np.setdiff1d(dates, toto)
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
		if len(toRequest) == 1: toRequest.append(toRequest[0])
		for row in range(1, len(toRequest)):
			#print "icicici", toRequest[row-1], toRequest[row]
			try: 
				fromyahoo = web.DataReader(name=BBG, data_source ='yahoo', start=toRequest[row-1], end=toRequest[row])
				fromyahoo['bbg'] = BBG
				fromyahoo.to_sql('spots', engine, if_exists='append') 
			except: print "yahoo request failed! ", BBG

def cTurbo(Fwd, strike, barrier, quot, margin):
	if Fwd > strike: return (Fwd - strike)/quot + margin
	else: 	return 0

def pTurbo(Fwd, strike, barrier, quot, margin):
	if strike > Fwd: return (strike - Fwd)/quot + margin
	else: 	return 0


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

