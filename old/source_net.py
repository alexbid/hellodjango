from module_yahoo.yahoo_finance import Share
import numpy as np
import pandas as pd
import pandas.io.data as web
import datetime

class getQuotes(Share):

	def get_historical_test(self):  #(self, start_date, end_date):
	
		startd = datetime.datetime(2015, 1, 1)
		endd = datetime.datetime(2015, 4, 13)
	
		#sp500 = web.DataReader('INDEXEURO:PX1', data_source ='google', start ='1/1/2000', end ='4/13/2015')
		
#		sp500 = web.DataReader('AMS:MT', data_source='google', start=startd, end=endd)
		sp500 = web.DataReader('AMS:MT', data_source='google', start=startd, end=endd)
		print sp500.info()
		print sp500		
		
		return sp500
		

if __name__=='__main__':
	print "dedede"
	x = getQuotes('^FTSE')
	x.get_historical_test()
