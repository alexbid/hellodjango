import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_batch.py','objects')
sys.path.append(addPath)

import numpy as np
import pandas as pds

from common import *
from sqlconnector import *

from dateutil.relativedelta import relativedelta

import stock, universe
		
if __name__=='__main__':
	flag = 'close'
	endDate = datetime.date.today()

	stDate = endDate + relativedelta(months=-11)
	windDate = endDate + relativedelta(days=-5)
	
	try:
		c = conn.cursor()
		c.execute("DELETE FROM hellodjango_signals")
		conn.commit()
#		conn.close()
	except:
		logging.info('Signals is not Empty...')

	x = universe.Universe()
	for i in range(0, len(x.listUniverse)):
		y = stock.Stock(x.listUniverse.BBG[i])
		y.load_pandas(stDate, endDate, flag)
		result1 = y.spots[(y.spots.index > windDate) & (y.spots.cv < 0.60/100 )]
		result1 = result1.drop('volume_20', 1)
		result1 = result1.drop('Volume', 1)
		result1['lastUpdate'] = datetime.datetime.utcnow()
		result2 = y.spots[(y.spots.index > windDate) & (y.spots.volume_20 * 5 < y.spots.Volume)]
		if len(result2.index) > 0:
			logging.info('results to be save in Excel %s', result2)
########	result2.to_excel('module_one/results/result_batch_volume_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
		if len(result1.index) > 0:
			logging.info('results to be save in DB %s', result1)
			#result1.to_excel('module_one/results/result_batch_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
			result1['BBG'] = x.listUniverse.BBG[i]
			try: result1.to_sql('hellodjango_signals', engine, if_exists='append')
			except AttributeError: logging.info('Not Save TO DB / run_batch.py')
		else: logging.info('nothing to save in DB')

