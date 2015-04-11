
import sys
import datetime
from module_one.code_python import Portfolio
from module_one.code_python import vTradingDates
from module_one.code_python import doRequestData


from dateutil.relativedelta import relativedelta

endDate = datetime.date.today()
stDate = endDate + relativedelta(months=-12)
evalDate = datetime.date(2015, 3, 31)
#windDate = endDate + relativedelta(days=-90)

from timeit import Timer
#t = Timer(lambda: vTradingDates(stDate, endDate, 'FR'))
#print t.repeat(3, 5)

doRequestData('^FCHI', stDate, endDate)
doRequestData('^GDAXI', stDate, endDate)
doRequestData('^FTSE', stDate, endDate)
portfolio = Portfolio()

portfolio.mDeposit(10000)
portfolio.load(stDate, evalDate)
print "portfolio values:", portfolio.getValue(evalDate,'close')
print "total fees:", portfolio.getFees()
print ""


	


