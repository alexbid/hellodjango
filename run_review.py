"""import datetime
import numpy as np
import pandas as pd
from module_one.code_python import Stock
from dateutil.relativedelta import relativedelta

endDate = datetime.date.today()
windDate = endDate + relativedelta(days=-300)
stDate = endDate + relativedelta(months=-11)

class graphy():
	
	def __init__(self, BBG):
		x = Stock(BBG)
		x.load_pandas(stDate, endDate, 'close')
		x.draw3(windDate, endDate)
		x.draw2(windDate, endDate)
	
	def toto(self):
		return "toto"

if __name__=='__main__':
#	#stDate = endDate + relativedelta(months=-11)
#	endDate = datetime.date.today()
#	windDate = endDate + relativedelta(days=-90)
#	stDate = endDate + relativedelta(months=-11)
#	#print windDate
	x = graphy('FP.PA')
#	x.load_pandas(stDate, endDate, 'close')
#	x.draw(windDate, endDate)

#sp500[[' Close', '42d', '252d']]. plot( grid = True, figsize =( 8, 5))
"""

from module_one.universe import Signals

if __name__=='__main__':
	
	y = Signals()
	y.graph_signals()