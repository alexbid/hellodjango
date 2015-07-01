import urllib
import re
import json
import datetime
from datetime import timedelta
import psycopg2
from module_one.code_python import sqlConnector

#htmltext = urllib.urlopen("http://www.bloomberg.com/markets/chart/data/1D/AAPL:US")
htmltext = urllib.urlopen("http://www.bloomberg.com/markets/chart/data/1D/CAC:IND")

data = json.load(htmltext)
datapoints = data['data_values']

sqlConn = sqlConnector()
c = sqlConn.conn.cursor()

for points in datapoints:
    tdate = datetime.datetime.fromtimestamp(points[0]/1000) + timedelta(hours=4)
    try:
		c.execute("""INSERT INTO intraday("bbg", "Last", "Date") VALUES(%s,%s,%s)""", ('^FCHI', float(points[1]), tdate) )

    except psycopg2.IntegrityError: print "quote already in DB Funds"
		
sqlConn.conn.commit()		
sqlConn.conn.close()

print len(datapoints)
#print datapoints

#print datapoints[len(datapoints)-1][1]