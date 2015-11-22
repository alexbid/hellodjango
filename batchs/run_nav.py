import sys
sys.path.insert(0, 'objects')

import psycopg2
import requests

#from module_one.code_python import sqlConnector
#from sqlalchemy import create_engine
#from module_one.universe import Universe
from datetime import time
import datetime
from common import *

import pandas as pds
import numpy as np
import universe

from lxml import html
from lxml import etree

x = universe.Universe()
univers = x.load_fund_nav()

for idx in range(len(univers)):
	#print univers['ISIN'].ix[idx] #, univ2, wkn
	wkn = str(univers['wkn'].ix[idx])
	page2 = requests.get('http://markets.ft.com/research//Tearsheets/PriceHistoryPopup?symbol=' + univers['ISIN'].ix[idx] + ':' + univers['CCY'].ix[idx])
	tree = html.fromstring(page2.text)

	dateList  = (tree.xpath("//tbody/tr/td[2]"))  #.replace('\n', '').strip()
	priceList = (tree.xpath("//tbody/tr/td[3]")) #last update
		
	npdateList = []
	nppriceList = []
	
	for item in priceList:
		nppriceList.append(item.text_content())


	for item in dateList:
		npdateList.append(datetime.datetime.strptime(str(item.text_content())+ ' 2015', '%B %d %Y'))
	
	npdateList = np.array(npdateList)
	nppriceList = np.array(nppriceList)
	
	s = pds.DataFrame(nppriceList, index=npdateList, columns=['NAV'])
	s.index.name = 'Date'
	s['wkn'] = wkn

	c = conn.cursor()
   
	minDate = s.index.min()
	maxDate = s.index.max()

	db = pds.read_sql("""SELECT DISTINCT "Date", "NAV", "wkn" FROM funds_nav WHERE "wkn"=%s ORDER BY "Date" ASC""", conn, index_col="Date", parse_dates=True, params=(wkn, ))
	toto = np.array(pds.to_datetime(db.index))
	tutu = np.array(pds.to_datetime(s.index))
	missingDates = np.setdiff1d(tutu, toto)

	print 'missingDates for ' + wkn + ': ', missingDates

	toDB = pds.DataFrame(s, index=missingDates)# , how='outer') #, lsuffix='_left', rsuffix='_right')
	toDB.index.name = 'Date'

	try:
		toDB.to_sql('funds_nav', engine, if_exists='append') 
	except psycopg2.IntegrityError:
		print "quote already in DB Funds"
	print wkn + '....done'


