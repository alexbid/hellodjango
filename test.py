

from module_one.code_python import sqlConnector

from pandas import *
from pandas.io.json import json_normalize
import pandas as pd
from datetime import timedelta
#from datetime import gmtime
from datetime import tzinfo
import pytz 

df = pd.read_json("http://www.bloomberg.com/markets/chart/data/1D/CAC:IND")
shift = 6

#from datetime import datetime, timedelta
#from pytz import timezone
#import pytz
#utc = pytz.utc

#ams_dt = loc_dt.astimezone(amsterdam)
#ams_dt.strftime(fmt)


#print df['exch_open_time'][0]+ timedelta(hours=shift), df['exch_close_time'][0]+ timedelta(hours=shift)
print df['exch_open_time'][0]+ timedelta(hours=shift), df['exch_close_time'][0] + timedelta(hours=shift)

#print df['data_values']
toot = pytz.timezone('Europe/Paris')

for points in df['data_values']:
    #tdate = datetime.fromtimestamp(points[0]/1000) + timedelta(hours=shift-2)
    #tdate = datetime.fromtimestamp(points[0]/1000) - datetime.utcfromtimestamp(points[0]/1000)
	tdate = datetime.utcfromtimestamp(points[0]/1000)
	print tdate, float(points[1]), datetime.fromtimestamp(points[0]/1000, tz=toot )
	#print tdate, float(points[1])

#print datetime.gmtime(), datetime.localtime()