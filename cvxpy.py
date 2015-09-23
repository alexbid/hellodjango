
from module_one.code_python import sqlConnector
import datetime
from datetime import time
import pandas as pds
import numpy as np
import scipy.optimize as sco
import xlrd
from sqlalchemy import create_engine
from dateutil.relativedelta import relativedelta
from operator import itemgetter

wkn_list = ['847101', '988562'] 
wkn = '847101'
engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')

class optimization():
	sqlConn = sqlConnector()
	endDate = datetime.date.today()
	stDate = endDate + relativedelta(weeks=-60)
	loadDate = stDate
	print stDate, endDate
		
	def __init__(self):
		self.noa = 0
		
		self.quarter = pds.DataFrame()
		self.rets = pds.DataFrame()
	
		self.idx = []
		self.nav = pds.DataFrame()
		self.time_ref_list = []
		
		self.nav = pds.read_sql("""SELECT "Date", "NAV", "wkn" FROM funds_nav WHERE (("Date" BETWEEN %s AND %s)) ORDER BY "Date" ASC;""", self.sqlConn.conn, index_col="Date", params=(self.loadDate, self.endDate))		
		for i in range(57): self.time_ref_list.append(datetime.timedelta(hours=8+ i//4, minutes=i%4*15)) 
		print 'loading optimization...'

	def load_data(self):
		#time_ref = datetime.timedelta(hours=8, minutes=0)
		symbols = ['^STOXX50E', '^FCHI', '^GSPC', '^FTSE', '^BVSP', '^RUT', '^GDAXI', '^SSMI', '^IBEX']
		"""
		^AEX
		1       ATX:IND        ^ATX
		2       CAC:IND       ^FCHI
		3      CCMP:IND       ^IXIC
		4       DAX:IND      ^GDAXI
		5   FTSEMIB:IND  FTSEMIB.MI
		6       HSI:IND        ^HSI
		7      IBEX:IND       ^IBEX
		8      IBOV:IND       ^BVSP
		9      INDU:IND        ^DJI
		10      NKY:IND       ^N225
		11      OMX:IND     ^OMXSPI
		12      RAY:IND        ^RUA
		13      RTY:IND        ^RUT
		14   SBF250:IND     ^SBF250
		15      SMI:IND       ^SSMI
		16      SPX:IND       ^GSPC
		17     SX5E:IND   ^STOXX50E
		18      UKX:IND       ^FTSE
		"""
		self.noa = len(symbols)+1

		data = pds.DataFrame()
		df1 = pds.DataFrame()
		for sym in symbols:
			print 'loading ' + sym
			data = pds.read_sql("""SELECT "Date", "Last" FROM intraday WHERE (("Date" BETWEEN %s AND %s) and ("bbg" = %s)) ORDER BY "Date" ASC;""", self.sqlConn.conn, index_col="Date", params=(self.loadDate, self.endDate, sym))
			data.columns = [sym,]
			df1 = pds.merge(data, df1,  left_index=True, right_index=True, how='outer')

		self.quarter = df1.resample(rule='15min', how='last', closed = 'right', label='left', loffset='15min', fill_method='ffill') 
	
	def load_data2(self):
		time_ref = datetime.timedelta(hours=8, minutes=0)
		symbols = ['^STOXX50E', '^FCHI', '^GSPC', '^FTSE', '^BVSP', '^RUT', '^GDAXI', '^SSMI', '^IBEX']
		self.noa = len(symbols)+1
		data = pds.DataFrame()
		df1 = pds.DataFrame()
		data = pds.read_sql("""SELECT "Date", "Last", "bbg" FROM intraday WHERE (("Date" BETWEEN %s AND %s)) ORDER BY "Date" ASC;""", self.sqlConn.conn, index_col="Date", params=(self.loadDate, self.endDate))
		print data
		self.quarter = df1.resample(rule='15min', how='last', closed = 'right', label='left', loffset='15min', fill_method='ffill') 
		
	def statistics(self, weights):
		"""
		Returns portfolio statistics. 
		Parameters 
		= = = = = = = = = = 
		weights : array-like weights for different securities in portfolio 
		Returns
		= = = = = = = 
		pret : float expected portfolio return 
		pvol : float expected portfolio volatility 
		pret / pvol : float Sharpe ratio for rf = 0
		"""
		
		weights = np.array(weights)
		#print 'rets.mean(): ', self.rets
		pret = np.sum(self.rets.mean() * weights) * 252
		pvol = np.sqrt( np.dot( weights.T, np.dot( self.rets.cov() * 252, weights))) 
		return np.array([ pret, pvol, pret / pvol])

	def min_func_sharpe(self, weights): return -self.statistics(weights)[2]
	def min_func_var(self, weights): return self.statistics(weights)[1]

	def getWeights(self, time_ref):

		index1 = pds.date_range(self.stDate + time_ref, self.endDate + time_ref, freq='D')
		df = pds.DataFrame(self.quarter, index = index1).dropna()
		df = df.resample('D', how='last')
		
		nav2 = pds.DataFrame(self.nav[self.nav['wkn']==wkn]['NAV'], index=self.nav[self.nav['wkn']=='847101'].index)
		df2 =  pds.merge(nav2, df,  left_index=True, right_index=True, how='outer')
		df = pds.DataFrame(df2 , index=df.index).dropna()
		
		self.rets = np.log(df / df.shift(1))
		self.idx = list(df.columns.values)

		cons = ({'type': 'eq', 'fun': lambda x: np.sum(x)})
		bnds = tuple(((-1, -1),)) + tuple([(0,1) for x in range(self.noa-1)]) 	
		weight_init =  self.noa * [1. / (self.noa-1),]
		weight_init[0] = -1

		#print 'bnds: ', bnds
		#print 'weight_init:', weight_init
		#print (weight_init)
		opts = sco.minimize(self.min_func_var, weight_init, method ='SLSQP', bounds = bnds, constraints = cons)
		#print opts
		#print symbols
		#print 'optimized weights: ',opts['x'].round(3)
		#print 'equiweighted: ', self.statistics(weight_init).round(3)
		#print 'optimised: ', self.statistics(opts['x']).round(3)
		return (opts['x']).round(3)
		
	def optimizeDate(self):
		result_List = []
		for i in range(6, 24): 
			result_List.append(self.optimizeTime(i))
		print min(result_List, key=itemgetter(1))

	def optimizeTime(self, nb_weeks):
		covar_ref_list = []
		weights_list = []
		stDate = self.endDate + relativedelta(weeks=-nb_weeks)

		for time_ref in self.time_ref_list:
			w = X.getWeights(time_ref)
			weights_list.append(w)
			covar_ref_list.append(X.statistics(w)[1])
			#print time_ref, w, X.statistics(w)
		#print time_ref_list
		#print covar_ref_list
		results = pds.DataFrame(covar_ref_list, index=self.time_ref_list, columns = ['VAR'])
		results['weights'] = weights_list
		
		print "NAV Time: ", results['VAR'].idxmin(), results['VAR'].min()
		#print "Weights: ", results[results['VAR'].idxmin()]

		print "NAV Time", results.ix[results['VAR'].idxmin()]
		#print X.idx 
		#print 'ty', results.ix[results['VAR'].idxmin()][1]
		resultss = pds.DataFrame(results.ix[results['VAR'].idxmin()][1],index=X.idx, columns = ['wght'])
		resultss.index.name = 'bbg'
		#resultss['updated'] = datetime.date(datetime.utcnow())
		resultss['updated'] = datetime.datetime.utcnow()
		resultss['basket_id'] = datetime.datetime.utcnow().strftime("%s")
		resultss['wkn'] = wkn
		resultss['var'] = results['VAR'].min()
		resultss['nb_weeks'] = nb_weeks
		return [resultss, results['VAR'].min()]
		
#resultss.to_sql('tracking_baskets', engine, if_exists='append') 
		#print list(X.df.columns.values)
		#Y = optimization()
		#Y.load_data()
		#print time_ref, Y.getWeights(datetime.timedelta(hours=22, minutes=0))
		#print getWeights(datetime.timedelta(hours=16, minutes=0))
	
if __name__=='__main__':
	X = optimization()
	X.load_data()
	#print X.optimizeTime(6)
	print X.optimizeDate()
	
	

