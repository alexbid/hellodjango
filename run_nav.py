
import psycopg2
from module_one.code_python import sqlConnector
from sqlalchemy import create_engine
from module_one.universe import Universe
from datetime import time
import pandas as pd
import numpy as np

from lxml import html
import requests
from datetime import datetime
import psycopg2
#from hellodjango.module_one.code_python import sqlConnector
from lxml import etree

#headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome", "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}

x = Universe()
univers = x.load_fund_nav()

#print len(univers)

for idx in range(len(univers)):
	#print univers['ISIN'].ix[idx] #, univ2, wkn
	wkn = str(univers['wkn'].ix[idx])
	page2 = requests.get('http://markets.ft.com/research//Tearsheets/PriceHistoryPopup?symbol=' + univers['ISIN'].ix[idx] + ':' + univers['CCY'].ix[idx])
	tree = html.fromstring(page2.text)

	dateList  = (tree.xpath("//tbody/tr/td[2]"))  #.replace('\n', '').strip()
	priceList = (tree.xpath("//tbody/tr/td[3]")) #last update
		
	npdateList = []
	nppriceList = []
	
	u = 0
	for item in priceList:
		#print u, (item.text_content())
		nppriceList.append(item.text_content())
		u += 1

	for item in dateList:
		#print u, (item.text_content())
		npdateList.append(datetime.strptime(str(item.text_content())+ ' 2015', '%B %d %Y'))
		u += 1
	
	npdateList = np.array(npdateList)
	nppriceList = np.array(nppriceList)
	
	s = pd.DataFrame(nppriceList, index=npdateList, columns=['NAV'])
	s.index.name = 'Date'
	s['wkn'] = wkn
	#print s
	sqlConn = sqlConnector()
	c = sqlConn.conn.cursor()
   
	minDate = s.index.min()
	maxDate = s.index.max()

	db = pd.read_sql("""SELECT DISTINCT "Date", "NAV", "wkn" FROM funds_nav WHERE "wkn"=%s ORDER BY "Date" ASC""", sqlConn.conn, index_col="Date", parse_dates=True, params=(wkn, ))
	toto = np.array(pd.to_datetime(db.index))
	tutu = np.array(pd.to_datetime(s.index))
	missingDates = np.setdiff1d(tutu, toto)

	print 'missingDates for ' + wkn + ': ', missingDates

	toDB = pd.DataFrame(s, index=missingDates)# , how='outer') #, lsuffix='_left', rsuffix='_right')
	toDB.index.name = 'Date'

	engine = create_engine('postgres://awsuser:Newyork2012@awsdbinstance.c9ydrnvcm8aj.us-west-2.rds.amazonaws.com:5432/marketdb')
	try:
		toDB.to_sql('funds_nav', engine, if_exists='append') 
	except psycopg2.IntegrityError:
		print "quote already in DB Funds"
	print wkn + '....done'


