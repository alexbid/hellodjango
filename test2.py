from module_one.code_python import sqlConnector

from pandas import *
#from pandas.io.json import json_normalize
import pandas as pd
from datetime import timedelta

df = pd.read_json("http://www.bloomberg.com/markets/chart/data/1D/CAC:IND")
shift = 6

print df['exch_open_time'][0]+ timedelta(hours=shift), df['exch_close_time'][0] + timedelta(hours=shift)

for points in df['data_values']:
	tdate = datetime.utcfromtimestamp(points[0]/1000) + timedelta(hours=shift)
	print tdate, float(points[1])