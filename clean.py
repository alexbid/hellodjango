

%pylab
%matplotlib inline

from hellodjango.module_one.code_python import sqlConnector
import datetime
import pandas as pds
from sqlalchemy import create_engine

stDate = datetime.datetime(2015, 7, 1, 0,0,0)
endDate = datetime.datetime(2015, 7, 1, 23,0,0)

sqlConn = sqlConnector()
#resultss = pds.read_sql("""SELECT "toto", "Last" FROM
#(SELECT "Last", MAX("Date") AS toto FROM intraday WHERE ("Date" BETWEEN %s AND %s) GROUP BY "Last")
#AS DERIVEDTABLE ORDER BY "toto" ASC""", sqlConn.conn, index_col="toto", params=(stDate.strftime('%Y-%m-%d %H:%M:%S'), endDate.strftime('%Y-%m-%d %H:%M:%S')))

resultss = pds.read_sql("""(SELECT * FROM intraday WHERE ("Date" BETWEEN %s AND %s) ORDER BY "Date")""", sqlConn.conn, index_col="Date", params=(stDate.strftime('%Y-%m-%d %H:%M:%S'), endDate.strftime('%Y-%m-%d %H:%M:%S')))
#
#DELETE FROM intraday WHERE ("Date" BETWEEN '2015-07-01 00:00:00' AND '2015-07-01 23:00:00') AND "bbg" = '^FCHI'

#(SELECT * FROM intraday WHERE ("Date" BETWEEN '2015-07-01 00:00:00' AND '2015-07-01 23:00:00') ORDER BY "Date")
SELECT "toto", "Last" FROM 
(SELECT "Last", MAX("Date") AS toto FROM intraday WHERE ("Date" BETWEEN '2015-07-01 00:00:00' AND '2015-07-01 23:00:00') GROUP BY "Last")
AS DERIVEDTABLE ORDER BY "toto" ASC

print resultss

#Last = resultss['Last']
#resultss.index.name = 'Date'
resultss['bbg'] = '^FCHI'
#print stDates
#groups = resultss.groupby(['Last'])
#print resultss
 
engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
try:
    resultss.to_sql('intraday', engine, if_exists='append') 
except psycopg2.IntegrityError:
    print "Oh no!!"

