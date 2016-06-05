
import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_clean.py','objects')
sys.path.append(addPath)

from common import *

import datetime
import pandas as pds

stDate = datetime.datetime(2015, 7, 1, 0,0,0)
endDate = datetime.datetime(2015, 7, 1, 23,0,0)

resultss = pds.read_sql("""(SELECT * FROM intraday WHERE ("Date" BETWEEN %s AND %s) ORDER BY "Date")""", conn, index_col="Date", params=(stDate.strftime('%Y-%m-%d %H:%M:%S'), endDate.strftime('%Y-%m-%d %H:%M:%S')))

logging.info('Results are %s', resultss)


resultss['bbg'] = '^FCHI'

try: resultss.to_sql('intraday', engine, if_exists='append') 
except psycopg2.IntegrityError:
    logging.info('Oh no!! Cannot connect to SQL-DB!!')

