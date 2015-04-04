
import sys
import datetime
from module_one.code_python import Portfolio
from module_one.code_python import vTradingDates
from module_one.code_python import doRequestData

dt = datetime.date(2014, 12, 30)
end = datetime.date(2015, 12, 31)

from timeit import Timer
#t = Timer(lambda: vTradingDates(dt, end, 'FR'))
#print t.repeat(3, 5)

doRequestData('^FCHI', dt, end)
portfolio = Portfolio()

portfolio.mDeposit(10000)
evalDate = datetime.date(2015, 3, 13)
portfolio.load(datetime.date(2000, 01, 26), evalDate)
print "portfolio values:", portfolio.getValue(evalDate,'close')
print "total fees:", portfolio.getFees()
print ""

#from hellodjango.views import getLastClose
#print str(getLastClose())

	


