
from datetime import timedelta
from datetime import *
import psycopg2
from module_one.code_python import sqlConnector
from sqlalchemy import create_engine

import pandas as pd
import numpy as np

shift = 6

df = pd.read_json("http://www.bloomberg.com/markets/chart/data/1D/CAC:IND")['data_values']
df = np.array(df)

sqlConn = sqlConnector()
c = sqlConn.conn.cursor()
dateArray = []
spotArray = []
shift = 4

for points in df:
<<<<<<< HEAD
    tdate = datetime.fromtimestamp(points[0]/1000) + timedelta(hours=shift)
=======
    tdate = datetime.utcfromtimestamp(points[0]/1000) + timedelta(hours=shift)
>>>>>>> 2e23cfcc1efc024851129ba40ee8bfaeeab53459
    dateArray.append(tdate)
    spotArray.append(float(points[1]))
   
s = pd.DataFrame(spotArray, index = dateArray, columns=['Last'])
s.index.name = 'Date'
s['bbg'] = '^FCHI'

minDate = s.index.min()
maxDate = s.index.max()

db = pd.read_sql("""SELECT "Date", "Last","bbg" FROM intraday WHERE ("Date" BETWEEN %s AND %s) ORDER BY "Date" ASC""", sqlConn.conn, index_col="Date", parse_dates=True, params=(minDate.strftime("%Y-%m-%d %H:%M:%S"), maxDate.strftime("%Y-%m-%d %H:%M:%S")))

toto = np.array(pd.to_datetime(db.index))
tutu = np.array(pd.to_datetime(s.index))

missingDates = np.setdiff1d(tutu, toto)

print 'missingDates: ', missingDates
toDB = pd.DataFrame(s, index=missingDates)# , how='outer') #, lsuffix='_left', rsuffix='_right')
toDB.index.name = 'Date'

engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
try:
    toDB.to_sql('intraday', engine, if_exists='append') 
except psycopg2.IntegrityError:
	print "quote already in DB Funds"
print '....done'