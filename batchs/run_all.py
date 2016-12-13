
#$1 can take:
#CRITICAL
#ERROR
#WARNING
#INFO
#DEBUG

import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_all.py','objects')
sys.path.append(addPath)
#sys.path.insert(0, 'hellodjango/objects')

import datetime
import numpy as np
import pandas as pds

from common import *
import universe, stock

from dateutil.relativedelta import relativedelta
from timeit import Timer

endDate = datetime.date.today()
stDate = endDate + relativedelta(months=-11)
evalDate = endDate
windDate = endDate + relativedelta(days=-5)
flag = 'close'

if __name__=='__main__':
    
    x = universe.Universe()
    
    for i in range(0, len(x.listUniverse)):
        doRequestData(x.listUniverse.BBG[i], x.listUniverse.CDR[i], stDate, endDate)
#        raw_input()
        y = stock.Stock(x.listUniverse.BBG[i])
            if y.load_pandas(stDate, endDate, flag):
            result1 = y.spots[(y.spots.index > windDate) & (y.spots.cv < 0.60/100 )]
    #        result1 = y.spots[(y.spots.index > windDate)]
            result1 = result1.drop('volume_20', 1)
            result1 = result1.drop('Volume', 1)
            result1['lastUpdate'] = datetime.datetime.utcnow()
            result2 = y.spots[(y.spots.index > windDate) & (y.spots.volume_20 * 5 < y.spots.Volume)]
            if len(result2.index) > 0:
                    logging.info(result2)
    #        print result1
    #        print "it was result1!!"
            #result2.to_excel('module_one/results/result_batch_volume_' + datetime.date.today().strftime("%Y-%m-%d") + "_"+ x.listUniverse.BBG[i] + '.xls')
            if len(result1.index) > 0:
                logging.info(result1)
                result1['BBG'] = x.listUniverse.BBG[i]
                result1.to_sql('hellodjango_signals', engine, if_exists='append')
                raw_input()
