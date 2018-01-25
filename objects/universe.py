

import datetime
import pandas as pds

from common import *
from dateutil.relativedelta import relativedelta

import stock

class Universe(object):
	def Universe(self):
		return "Universe"
		
	def __init__(self):
#		try:
            self.listUniverse = pds.read_sql("""SELECT DISTINCT "BBG", "CDR" FROM stockscreener_batch_run WHERE "isWorking"=True AND "BBG"='EURUSD=X' ORDER BY "BBG" ASC""", conn)
            logging.info('universe.py >> self.listUniverse %s ', self.listUniverse)

#            self.listUniverse = list(sorted(set(self.listUniverse)))
#		except: print "error in loading Universe!"

	def load_fund_nav(self):
		listFundsNAV = pds.read_sql("""SELECT DISTINCT "ISIN", "CCY", "wkn" FROM funds_static WHERE "isUpdate"=True ORDER BY "ISIN" ASC""", conn)
		return listFundsNAV

class Signals(object):
	def Signals(self): return "Signals"
	def __init__(self): self.listSignals = pds.read_sql("""SELECT DISTINCT "BBG" FROM stockscreener_signals ORDER BY "BBG" ASC""", conn)
	def graph_signals(self):
		endDate = datetime.date.today()
		stDate = endDate + relativedelta(months=-11)
		windDate = endDate + relativedelta(days=-5)
		
		for i in range(0, len(self.listSignals)):
			BBG = self.listSignals['BBG'][i]
			x = stock.Stock(BBG)
			x.load_pandas(stDate, endDate, "Close")
			x.draw3(stDate, endDate)
			
			
if __name__=='__main__':
    
    print 'to be done...'


