from module_one.code_python import Stock
from module_one.code_python import sqlConnector
from module_one.code_python import vTradingDates
import datetime
import numpy as np
import pandas as pds
from module_one.universe import Universe
from pandas import DataFrame
from pandas import concat
from sqlalchemy import create_engine

class Share(Stock):
	
	def toto(self):
		return "toto"
		
if __name__=='__main__':
	flag = 'close'
	endDate = datetime.date.today()
	from dateutil.relativedelta import relativedelta
	stDate = endDate + relativedelta(months=-11)
	windDate = endDate + relativedelta(days=-5)

	engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
	
	try: 
		sqlConn = sqlConnector()
		c = sqlConn.conn.cursor()
		c.execute("DELETE FROM signals")
		sqlConn.conn.commit()
		sqlConn.conn.close()
	except: print "Signals is not Empty..."

	x = Universe()
	for i in range(0, len(x.listUniverse)):
		y = Share(x.listUniverse.BBG[i])
		y.load_pandas(stDate, endDate, flag)
		result1 = y.spots[(y.spots.index > windDate) & (y.spots.cv < 0.60/100 )]
		result1 = result1.drop('volume_20', 1)
		result1 = result1.drop('Volume', 1)
		result2 = y.spots[(y.spots.index > windDate) & (y.spots.volume_20 < y.lvolume )]
		if len(result2.index) > 0: 
			#result1.to_excel('module_one/results/result_batch_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
			result2.to_excel('module_one/results/result_batch_volume_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
		if len(result1.index) > 0: 
			print result1
			#result1.to_excel('module_one/results/result_batch_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
			result1['BBG'] = x.listUniverse.BBG[i]
			result1.to_sql('signals', engine, if_exists='append')
			#result1.to_sql('signals', engine, if_exists='replace')
