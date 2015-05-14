from code_python import Stock
from code_python import sqlConnector
#from code_python import vTradingDates
import datetime
#import numpy as np
#import pandas as pds
import pandas as pds
#from run_graph import graphy

class Universe(object):
	
	listUniverse = ""
	
	def Universe(self):
		return "Universe"
		
	def __init__(self):
		#try:
		sqlConn = sqlConnector()			
		self.listUniverse = pds.read_sql("""SELECT DISTINCT "BBG", "CDR" FROM batch_run WHERE "isWorking"=True ORDER BY "BBG" ASC""", sqlConn.conn)
		#except:
		#	print "error in loading Universe!"
#		sqlConn.conn.close()


class Signals(object):
	
	listSignals = ""

	def Signals(self):
		return "Signals"
		
	def __init__(self):
		sqlConn = sqlConnector()			
		self.listSignals = pds.read_sql("""SELECT DISTINCT "BBG" FROM hellodjango_signals ORDER BY "BBG" ASC""", sqlConn.conn)
		#self.listSignals = pds.read_sql("""SELECT DISTINCT "BBG", "CDR" FROM batch_run WHERE "isWorking"=True ORDER BY "BBG" ASC""", sqlConn.conn)
	
	def graph_signals(self):
	
		endDate = datetime.date.today()
		from dateutil.relativedelta import relativedelta
		stDate = endDate + relativedelta(months=-11)
		windDate = endDate + relativedelta(days=-5)
		
		#self.load_signals()
		
		for i in range(0, len(self.listSignals)):
			BBG = self.listSignals['BBG'][i]
			x = Stock(BBG)
			#print "stDate, endDate: ", stDate, endDate
			x.load_pandas(stDate, endDate, "Close")
			x.draw3(stDate, endDate)
			
			
#if __name__=='__main__':
#	flag = 'close'
#	endDate = datetime.date.today()
#	from dateutil.relativedelta import relativedelta
#	stDate = endDate + relativedelta(months=-11)
#	windDate = endDate + relativedelta(days=-5)
#	engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
#	x = Universe()
#	for i in range(0, len(x.listUniverse)):
"""		y = Share(x.listUniverse.BBG[i])
		y.load_pandas(stDate, endDate, flag)
		result1 = y.spots[(y.spots.index > windDate) & (y.spots.cv < 0.60/100 )]
		if len(result1.index) > 0: 
			print result1
			result1.to_excel('module_one/results/result_batch_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
			result1['BBG'] = x.listUniverse.BBG[i]
			result1.to_sql('signals', engine, if_exists='append')
			#result1.to_sql('signals', engine, if_exists='replace')
			
"""			
#			x = graphy(BBG)
#			x.draw3(stDate, endDate)
#			x.draw2(stDate, endDate)

	#def getUniverse(self):
	#	return self.BBG()
	#for line in BBG:
	#	try:
	#		x = Share(line)
	#		x.load_pandas(stDate, endDate, flag)
	#		result1 = x.spots[(x.spots.date > windDate) & (x.spots.cv < 0.25/100 )]
	#		print result1
	#	except:
	#		print "error in loading historic prices in batch for " + line