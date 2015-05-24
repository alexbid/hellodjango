

import sys
import datetime
#from module_one.code_python import Portfolio
from module_one.code_python import vTradingDates
from module_one.code_python import doRequestData
from module_one.code_python import Stock
from module_one.code_python import sqlConnector
import numpy as np
import pandas as pds
from module_one.universe import Universe
from pandas import DataFrame
from pandas import concat
from sqlalchemy import create_engine
from dateutil.relativedelta import relativedelta
from timeit import Timer

endDate = datetime.date.today()
stDate = endDate + relativedelta(months=-11)
evalDate = endDate
windDate = endDate + relativedelta(days=-5)
flag = 'close'

class Share(Stock):
	
	def toto(self):
		return "toto"

if __name__=='__main__':

	try: 
		sqlConn = sqlConnector()
		c = sqlConn.conn.cursor()
		c.execute("DELETE FROM hellodjango_signals")
		sqlConn.conn.commit()
		sqlConn.conn.close()
	except: print "Signals is not Empty..."

	engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')

	x = Universe()
	for i in range(0, len(x.listUniverse)):
		doRequestData(x.listUniverse.BBG[i], x.listUniverse.CDR[i], stDate, endDate)
		y = Share(x.listUniverse.BBG[i])
		y.load_pandas(stDate, endDate, flag)
		result1 = y.spots[(y.spots.index > windDate) & (y.spots.cv < 0.60/100 )]
		result1 = result1.drop('volume_20', 1)
		result1 = result1.drop('Volume', 1)
		result1['lastUpdate'] = datetime.datetime.utcnow()
		result2 = y.spots[(y.spots.index > windDate) & (y.spots.volume_20 * 5 < y.spots.Volume)]
		if len(result2.index) > 0: 
			print result2
########	result2.to_excel('module_one/results/result_batch_volume_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
		if len(result1.index) > 0: 
			print result1
			result1['BBG'] = x.listUniverse.BBG[i]
			result1.to_sql('hellodjango_signals', engine, if_exists='append')
