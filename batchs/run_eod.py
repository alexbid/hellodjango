
#$1 can take:
#CRITICAL
#ERROR
#WARNING
#INFO
#DEBUG

import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_eod.py','objects')
sys.path.append(addPath)

import datetime
import psycopg2
from common import *
from dateutil import tz
import pandas as pds
import numpy as np

shift = 6

def bloombergScrap(mnemo, ric):
    try:
        df = pds.read_json("http://www.bloomberg.com/markets/chart/data/1D/" + mnemo)['data_values']
        df = np.array(df)
    except:
        logging.error('cannot connect to webpage http://www.bloomberg.com/markets/chart/data/1D/%s => %s', mnemo, ric)
        return ''

	dateArray = []
	spotArray = []

	for points in df:
	#    tdate = datetime.fromtimestamp(points[0]/1000) + timedelta(hours=shift)
		tdate = datetime.datetime.utcfromtimestamp(points[0]/1000) + datetime.timedelta(hours=shift)
		dateArray.append(tdate)
		spotArray.append(float(points[1]))
   
	s = pds.DataFrame(spotArray, index = dateArray, columns=['Last'])
	s.index.name = 'Date'
	s['bbg'] = ric

	minDate = s.index.min()
	maxDate = s.index.max()

	db = pds.read_sql("""SELECT "Date", "Last","bbg" FROM intraday WHERE ("bbg"=%s AND ("Date" BETWEEN %s AND %s)) ORDER BY "Date" ASC""", conn, index_col="Date", parse_dates=True, params=(ric, minDate.strftime("%Y-%m-%d %H:%M:%S"), maxDate.strftime("%Y-%m-%d %H:%M:%S")))

	toto = np.array(pds.to_datetime(db.index))
	tutu = np.array(pds.to_datetime(s.index))
	missingDates = np.setdiff1d(tutu, toto)

	#from_zone = tz.tzutc()
	#to_zone = tz.tzlocal()
	#utc = utc.replace(tzinfo=from_zone)
	#missingDates = missingDates.replace(tzinfo=from_zone)
	#central = missingDates.astimezone(to_zone)

	logging.debug('missingDates for %s: %s', mnemo, missingDates)
	toDB = pds.DataFrame(s, index=missingDates)# , how='outer') #, lsuffix='_left', rsuffix='_right')
	toDB.index.name = 'Date'
#	logging.info('number of data to be saved: %s ', len(toDB.index))

	if len(toDB.index) > 0:
		try:
			toDB.to_sql('intraday', engine, if_exists='append')
		except psycopg2.IntegrityError:
			logging.info('quote already in DB Funds')
		except:
			logging.error('error in saving quote %s %s %s', mnemo, ric, toDB)
	else:
		logging.info('no data to be saved for quote %s %s ', mnemo, ric)

if __name__=='__main__':
    mnemoList = pds.read_sql("""SELECT DISTINCT "mnemo", "BBG" FROM stockscreener_batch_run WHERE "mnemo" IS NOT NULL ORDER BY "mnemo" ASC""", conn)

    for index, row in mnemoList.iterrows():
        bloombergScrap(row['mnemo'], row['BBG'])










