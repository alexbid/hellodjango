import sys
#sys.path.insert(0, 'objects')
sys.path.insert(0, 'hellodjango/objects')

import sys
import datetime

import universe, portfolio
from dateutil.relativedelta import relativedelta

endDate = datetime.date.today()
stDate = endDate + relativedelta(months=-11)
evalDate = endDate+ relativedelta(days=-1)

#from timeit import Timer
#t = Timer(lambda: vTradingDates(stDate, endDate, 'FR'))
#print t.repeat(3, 5)

#x = Universe()
#for i in range(0, len(x.listUniverse)):
#	doRequestData(x.listUniverse.BBG[i], x.listUniverse.CDR[i], stDate, endDate)
#doRequestData("^FCHI", "FR", stDate, endDate)

portf = portfolio.Portfolio()
portf.mDeposit(10000)
portf.load(stDate, evalDate)
print "portfolio values:", portf.getValue(evalDate,'close')
print "total fees:", portf.getFees()
print ""


	


