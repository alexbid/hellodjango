
import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_clean_calendar.py','objects')
sys.path.append(addPath)

from common import *

import datetime
import pandas as pds


calendar = pds.read_sql("""SELECT distinct cdr FROM stockscreener_calendar;""", conn)

for cal in calendar['cdr']:
	stockscreener_calendar_doclean(cal)
logging.info('batchs/run_clean_calendar.py done....')