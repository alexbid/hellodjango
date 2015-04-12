import datetime
import numpy as np
import pandas as pd
from module_one.code_python import Stock


if __name__=='__main__':
	from dateutil.relativedelta import relativedelta
	#stDate = endDate + relativedelta(months=-11)
	endDate = datetime.date.today()
	windDate = endDate + relativedelta(days=-90)
	stDate = endDate + relativedelta(months=-11)
	
	#print windDate
	
	x = Stock('^FCHI')
	x.load_pandas(stDate, endDate, 'close')
	x.draw2(windDate, endDate)

#sp500[[' Close', '42d', '252d']]. plot( grid = True, figsize =( 8, 5))
