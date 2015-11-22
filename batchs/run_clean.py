
import sys
sys.path.insert(0, 'objects')

from common import *
#from hellodjango.module_one.code_python import sqlConnector

import datetime
import pandas as pds
#from sqlalchemy import create_engine

stDate = datetime.datetime(2015, 7, 1, 0,0,0)
endDate = datetime.datetime(2015, 7, 1, 23,0,0)

resultss = pds.read_sql("""(SELECT * FROM intraday WHERE ("Date" BETWEEN %s AND %s) ORDER BY "Date")""", conn, index_col="Date", params=(stDate.strftime('%Y-%m-%d %H:%M:%S'), endDate.strftime('%Y-%m-%d %H:%M:%S')))

print resultss

resultss['bbg'] = '^FCHI'

try: resultss.to_sql('intraday', engine, if_exists='append') 
except psycopg2.IntegrityError:
    print "Oh no!! Cannot connect to SQL-DB!!"

