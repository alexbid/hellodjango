#from code_python import Stock
from code_python import sqlConnector
#from code_python import vTradingDates
#import datetime
#import numpy as np
#import pandas as pds

class Universe(object):
	
	listUniverse = ""
	
	def Universe(self):
		return "Universe"
		
	def __init__(self):
		import pandas as pds
		try:
			sqlConn = sqlConnector()			
			self.listUniverse = pds.read_sql("SELECT * FROM batch_run", sqlConn.conn)
		except:
			print "error in loading Universe!"
#		sqlConn.conn.close()
	
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