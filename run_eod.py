
from datetime import timedelta
from datetime import *
import psycopg2
from module_one.code_python import sqlConnector
from sqlalchemy import create_engine

from dateutil import tz
import pandas as pd
import numpy as np

shift = 6

sqlConn = sqlConnector()
c = sqlConn.conn.cursor()

def bloombergScrap(mnemo, ric):

	df = pd.read_json("http://www.bloomberg.com/markets/chart/data/1D/" + mnemo)['data_values']
	df = np.array(df)

	dateArray = []
	spotArray = []

	for points in df:
	#    tdate = datetime.fromtimestamp(points[0]/1000) + timedelta(hours=shift)
		tdate = datetime.utcfromtimestamp(points[0]/1000) + timedelta(hours=shift)
		dateArray.append(tdate)
		spotArray.append(float(points[1]))
   
	s = pd.DataFrame(spotArray, index = dateArray, columns=['Last'])
	s.index.name = 'Date'
	s['bbg'] = ric

	minDate = s.index.min()
	maxDate = s.index.max()

	db = pd.read_sql("""SELECT "Date", "Last","bbg" FROM intraday WHERE ("bbg"=%s AND ("Date" BETWEEN %s AND %s)) ORDER BY "Date" ASC""", sqlConn.conn, index_col="Date", parse_dates=True, params=(ric, minDate.strftime("%Y-%m-%d %H:%M:%S"), maxDate.strftime("%Y-%m-%d %H:%M:%S")))

	toto = np.array(pd.to_datetime(db.index))
	tutu = np.array(pd.to_datetime(s.index))
	missingDates = np.setdiff1d(tutu, toto)

	#from_zone = tz.tzutc()
	#to_zone = tz.tzlocal()
	#utc = utc.replace(tzinfo=from_zone)
	#missingDates = missingDates.replace(tzinfo=from_zone)
	#central = missingDates.astimezone(to_zone)

	print 'missingDates for ' + mnemo + ': ', missingDates
	
	#raw_input()
	toDB = pd.DataFrame(s, index=missingDates)# , how='outer') #, lsuffix='_left', rsuffix='_right')
	toDB.index.name = 'Date'

	engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
	try:
		toDB.to_sql('intraday', engine, if_exists='append') 
	except psycopg2.IntegrityError:
		print "quote already in DB Funds"
	print mnemo + '....done'
	
mnemoList = pd.read_sql("""SELECT DISTINCT "mnemo", "BBG" FROM batch_run WHERE "mnemo" IS NOT NULL ORDER BY "mnemo" ASC""", sqlConn.conn)	
#print mnemoList
for index, row in mnemoList.iterrows():
	bloombergScrap(row['mnemo'], row['BBG'])


#for imnemo in mnemoList['mnemo']:
	#bloombergScrap(imnemo)







