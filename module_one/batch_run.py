from code_python import Stock
from code_python import sqlConnector
from code_python import vTradingDates
import datetime
import numpy as np
import pandas as pds
#from module_one.universe import Universe
from universe import Universe
from pandas import DataFrame
from pandas import concat

#import pandas.io.sql as pds

class Share(Stock):
	
	def toto(self):
		return "toto"
		
if __name__=='__main__':
	flag = 'close'
	endDate = datetime.date.today()
	from dateutil.relativedelta import relativedelta
	stDate = endDate + relativedelta(months=-11)
	windDate = endDate + relativedelta(days=-5)

	x = Universe()
	#result0 = pds.DataFrame()
	for i in range(0, len(x.listUniverse)):
		#try:
		y = Share(x.listUniverse.BBG[i])
		y.load_pandas(stDate, endDate, flag)
#		result1 = y.spots[(y.spots.date > windDate) & (y.spots.cv < 0.60/100 )]
		#print "y.spots: ", y.spots
		result1 = y.spots[(y.spots.index > windDate) & (y.spots.cv < 0.60/100 )]
		if len(result1.index) > 0: 
			#print "signal"
			#if len(result0.index) > 0: 
			#	print result0
			#	result0 = pds.merge(result0, result1) #, left_on='lkey', right_on='rkey', how='outer')
			#else:
			#	result0 = result1
			print result1
			result1.to_excel('results/result_batch_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
		#except:
		#	print "error in loading historic prices in batch for " + x.listUniverse.BBG[i]
	
	#sqlConn.conn.close()


	#startdt = datetime.date(2015, 01, 01)
	#enddt = datetime.date(2015, 4, 10)

	#x = Share("^FCHI")
	#a = np.array([ 0, 0.5, 1.0, 1.5, 2.0])
	#print a.sum()
	#print a.std()
	#x.load_pandas(startdt, enddt, 'close')
	
	#res = x.spots#[:: 100] # every 100th result

	#yhoo = res[['date', 'spot', 'mavg_30', 'ewma_10', 'ewma_20', 'ewma_50', 'ewma_100']]
	#print yhoo
	#import matplotlib.pyplot as plt 
	#plt.title('Graph: ' + x.getMnemo() )
	#yhoo['spot'].plot(label='CAC40')
	#yhoo['mavg_30'].plot(label='mavg_30')
	#yhoo['ewma_10'].plot(label='ewma_10')
	#yhoo['ewma_20'].plot(label='ewma_20')
	#yhoo['ewma_50'].plot(label='ewma_50')
	#yhoo['ewma_100'].plot(label='ewma_100')
	#plt.xlabel(yhoo['date'])
#	yhoo.plot.plot(style='r', lw = 2.)
#	yhoo['spot'].plot(figsize =( 8, 5))
	#plt.legend()
	#plt.show()