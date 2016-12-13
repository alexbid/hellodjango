import datetime
import calendar
import pdb
import os

import pandas as pds
import numpy as np
#import pandas.io.data as web
#from pandas_datareader import data, wb
#.data as web
import pandas_datareader.data as web

import logging
logging.basicConfig(level='DEBUG' , format='%(asctime)s - %(levelname)s - %(message)s')

from sqlconnector import *
calendar.setfirstweekday(calendar.MONDAY)

import portfolio

##########################################################
#import sys
#sys.path.append('~/module_yahoo/yahoo_finance')
#from module_yahoo.yahoo_finance import Share
#from yahoo_finance import get_historical
##########################################################

def isWeekEnd(tDate):
    if tDate.weekday() == 5 or tDate.weekday() == 6: return True
    else: return False

def isTradingDay(tDate):
    if isWeekEnd(tDate): return False
    else:
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM calendar WHERE date = %s', (tDate.strftime("%Y-%m-%d"),))
        data = c.fetchone()[0]
        if data == 0:
            print('this is a trading day ' + tDate.isoformat())
            c.close()
            return True
        else:
            print('this is a HOLIDAY! ' + tDate.isoformat())
            c.close()
            return False

def calendar_clean(theDates, CAL):
    theDates = np.array(theDates.to_datetime())
    c = conn.cursor()
    holi = pds.read_sql("SELECT date FROM calendar WHERE (CDR=%s) AND (date BETWEEN %s AND %s) ORDER BY date ASC", conn, index_col='date', params=(CAL, pds.to_datetime(theDates[0]).strftime('%Y-%m-%d'), pds.to_datetime(theDates[-1]).strftime('%Y-%m-%d')))
    holi = np.array(pds.to_datetime(holi.index))
    return np.setdiff1d(theDates, holi)

def vTradingDates(stDate, endDate, cdr):
    c = conn.cursor()
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
    c.close()
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
    lstTDR = endD
    if endD >= refDate: 
        if np.is_busday(refDate):
            if refHour > 6: lstTDR = np.busday_offset(refDate, -1, roll='backward')
            else: lstTDR = np.busday_offset(endD, -2, roll='backward')
        else:
            if refHour > 6: lstTDR = np.busday_offset(refDate, 0, roll='backward')
            else: lstTDR = np.busday_offset(endD, -2, roll='backward')
    buff = pds.to_datetime(lstTDR)
    return buff

def getRequestDateList(tempAlex):
    toRequest = []
    if len(tempAlex) > 0:
        row = [pds.to_datetime(tempAlex[0]).date(), pds.to_datetime(tempAlex[-1]).date()]
        toRequest.append(row)
    else: return None

    return toRequest

def doRequestData(BBG, CAL, startD, endD):
    from datetime import date
    endD = getLastTrDay(endD)
    logging.info('doRequestData %s %s', BBG, endD)
#############################################################################################################################
    # remove holidays from dates in input
    dates = calendar_clean(pds.date_range(start=startD, end=endD, freq ='1B').to_datetime(), CAL)
    c = conn.cursor()
#############################################################################################################################   
    # get dates already in the DB
    flag = 'Close'
    fromdb = pds.read_sql("""SELECT "Date", "Close" FROM spots WHERE BBG=%s AND ("Date" BETWEEN %s AND %s)""", conn, index_col="Date", params=(BBG, startD, endD), parse_dates=True)
    toto = np.array(pds.to_datetime(fromdb.index))
    # get list of dates to retrieve
    tempAlex = np.setdiff1d(dates, toto)
### optimisation du nombre de requete Yahoo #################################################################################
    toRequest = getRequestDateList(tempAlex)
### save to DB ##############################################################################################################
    if toRequest:
        logging.info('Period To Request for Stock: %s %s %s', BBG, toRequest, len(toRequest))
        for row in toRequest:
            try:
#            if True:
                fromyahoo = web.DataReader(name=BBG, data_source ='yahoo', start=row[0], end=row[1])
                fromyahoo['bbg'] = BBG
                fromyahoo.to_sql('spots', engine, if_exists='append')
            except:
                logging.error('yahoo failed! %s %s %s', BBG, toRequest, len(toRequest))

def cTurbo(Fwd, strike, barrier, quot, margin):
    if Fwd > strike: return (Fwd - strike)/quot + margin
    else:   return 0

def pTurbo(Fwd, strike, barrier, quot, margin):
    if strike > Fwd: return (strike - Fwd)/quot + margin
    else:   return 0


if __name__=='__main__':
    import sys
    dt = datetime.date(1990, 03, 01)
    end = datetime.date(2014, 12, 30)

    from timeit import Timer
#    t = Timer(lambda: vTradingDates(dt, end, 'FR'))
    #print t.timeit(number=1)
#    print t.repeat(3, 5)
    doRequestData('^FCHI', 'FR', dt, end)
    #print vTradingDates(dt, end, 'FR')
    #print cTurbo(4346, 3750, 3750, 100.0, 0.08)
    #print pTurbo(4346, 4500, 4500, 100.0, 0.08)
    #x = Stock("^FCHI")
    #print x.spot
    #print x.getClose(datetime.date(1999, 1, 5))
    portf = portfolio.Portfolio()
    #tDate = datetime.date(1999, 1, 5)
    #portfolio.trade(tDate, x, 1, x.getClose(tDate), 10)
    #portfolio.trade(tDate, x, 1, x.getClose(tDate), 10)
    portf.mDeposit(10000)
    #print "value at trade date:", portfolio.getValue(tDate,'close')
    #print "value as of today: ", portfolio.getValue(datetime.date(2014, 11, 26),'close')
    #print "gain: ", portfolio.getValue(datetime.date(2014, 11, 26),'close')-portfolio.getValue(tDate,'close')
    evalDate = datetime.date(2015, 04, 04)
    portf.load(datetime.date(2000, 01, 26), evalDate)
    print "portfolio values:", portf.getValue(evalDate,'close')
    print "total fees:", portf.getFees()

