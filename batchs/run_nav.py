import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_nav.py','objects')
sys.path.append(addPath)

import psycopg2
import requests

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
session = requests.Session()

headers = {"User-Agent":"Mozilla/ 5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome", "Accept":"text/html, application/xhtml+xml, application/xml; q=0.9, image/webp,*/*;q=0.8"}

for idx in range(len(univers)):
	wkn = str(univers['wkn'].ix[idx])

    url = 'http://markets.ft.com/research//Tearsheets/PriceHistoryPopup?symbol=' + univers['ISIN'].ix[idx] + ':' + univers['CCY'].ix[idx]

	try:
        page2 = session.get(url, headers = headers)
        tree = html.fromstring(page2.text)

        dateList  = (tree.xpath("//tbody/tr/td/span[1]"))  #.replace('\n', '').strip()
		priceList = (tree.xpath("//tbody/tr/td[3]")) #last update
        
		npdateList = []
		nppriceList = []
        
		for item in priceList: nppriceList.append(item.text_content())
        
		logging.debug('%s', dateList[0].text_content())
        
		for item in dateList:
			try:
				logging.info('dateList strptime item %s', datetime.datetime.strptime(str(item.text_content()), '%A, %B %d, %Y'))
				npdateList.append(datetime.datetime.strptime(str(item.text_content()), '%A, %B %d, %Y'))
			except:
				pass

		npdateList = np.array(npdateList)
		nppriceList = np.array(nppriceList)

		logging.debug('%s %s ', len(npdateList) , len(npdateList))

		if len(npdateList) == len(npdateList):
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
        
        		logging.info('missingDates for %s: %s', wkn, missingDates)
        
        		toDB = pds.DataFrame(s, index=missingDates)# , how='outer') #, lsuffix='_left', rsuffix='_right')
        		toDB.index.name = 'Date'
        
        		try: toDB.to_sql('funds_nav', engine, if_exists='append')
        		except psycopg2.IntegrityError: logging.error('quote already in DB Funds')
        		logging.info('%s ......done', wkn)
		else: logging.error('error with %s, nb of dates and prices do not match!!', wkn)

	except requests.exceptions.ConnectionError:
		logging.error('Connection refused')
		pass



