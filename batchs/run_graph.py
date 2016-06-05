
import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_graph.py','objects')
sys.path.append(addPath)

import datetime
import numpy as np
import pandas as pds
from common import *

from dateutil.relativedelta import relativedelta

import stock 
endDate = datetime.date.today()
windDate = endDate + relativedelta(days=-300)
stDate = endDate + relativedelta(months=-11)

class graphy():
	
	def __init__(self, BBG):
		x = stock.Stock(BBG)
        logging.debug('%s: %s', type(stDate), type(endDate))

		x.load_pandas(stDate, endDate, 'Close')
		x.draw3(windDate, endDate)
		#x.draw2(windDate, endDate)

if __name__=='__main__':
#	#stDate = endDate + relativedelta(months=-11)
#	endDate = datetime.date.today()
#	windDate = endDate + relativedelta(days=-90)
#	stDate = endDate + relativedelta(months=-11)
	x = graphy('TES.PA')
#	x.load_pandas(stDate, endDate, 'close')
#	x.draw(windDate, endDate)

#sp500[[' Close', '42d', '252d']]. plot( grid = True, figsize =( 8, 5))
