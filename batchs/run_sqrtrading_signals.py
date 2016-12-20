import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_sqrtrading_signals.py','objects')
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
		c.execute("DELETE FROM stockscreener_signals")
		conn.commit()
#		conn.close()
	except:
		logging.info('Signals is not Empty...')

	x = universe.Universe()
	for i in range(0, len(x.listUniverse)):
		BBG = x.listUniverse.BBG[i]
		y = stock.Stock(x.listUniverse.BBG[i])
		if y.load_pandas(stDate, endDate, flag):
			result1 = y.spots[(y.spots.index > windDate) & (y.spots.cv < 0.60/100 )]
			result1 = result1.drop('volume_20', 1)
			result1 = result1.drop('Volume', 1)
			result1['lastUpdate'] = datetime.datetime.utcnow()
#			result2 = y.spots[(y.spots.index > windDate) & (y.spots.volume_20 * 5 < y.spots.Volume)]
#			if len(result2.index) > 0:
#				logging.info('results to be save in Excel %s', result2)
#				result2.to_excel('module_one/results/result_batch_volume_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
			if len(result1.index) >= 1:
#				logging.info('results to be save in DB %s', result1)
				#result1.to_excel('module_one/results/result_batch_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
				result1['BBG'] = x.listUniverse.BBG[i]
				result1 = result1.tail(1)
				try:
					result1.to_sql('stockscreener_signals', engine, if_exists='append')
					logging.info('results saved in DB %s', BBG)
				except AttributeError:
					logging.info('Not Save TO DB / run_sqrtrqding_signals.py')
			#elif len(result1.index) > 1:
			#	result1['BBG'] = x.listUniverse.BBG[i]
			#	print result1.tail(1)
			#	result1.to_sql('stockscreener_signals', engine, if_exists='append')
			#	logging.error('ERROR in run_sqrtrqding_signals.py // several results inscreenoing for the stock %s', BBG)
			#	logging.error('ERROR len(result1) %s %s', len(result1), result1)
			#	pass
			else:
				logging.debug('nothing to save in DB')


