
import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_valo.py','objects')
sys.path.append(addPath)

import datetime
from common import *

import universe, portfolio
from dateutil.relativedelta import relativedelta

endDate = datetime.date.today()
# endDate = datetime.date(2017, 12, 31)
stDate = endDate + relativedelta(months=-11)
evalDate = endDate+ relativedelta(days=-1)

#from timeit import Timer
#t = Timer(lambda: vTradingDates(stDate, endDate, 'FR'))
# logging.info('%s', t.repeat(3, 5))


#x = Universe()
#for i in range(0, len(x.listUniverse)):
#	doRequestData(x.listUniverse.BBG[i], x.listUniverse.CDR[i], stDate, endDate)
#doRequestData("^FCHI", "FR", stDate, endDate)

portf = portfolio.Portfolio()
portf.mDeposit(1000)
portf.load(stDate, evalDate)

logging.info('portfolio values: %s', portf.getValue(evalDate,'close'))
logging.info('total fees: %s', portf.getFees())
