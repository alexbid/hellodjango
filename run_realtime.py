from lxml import html
import requests
from datetime import datetime
import psycopg2

from module_one.code_python import sqlConnector

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome", "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}

page2 = requests.get('https://www.boerse-stuttgart.de/de/boersenportal/wertpapiere-und-maerkte/fonds/factsheet/?ID_NOTATION=15314068', headers = headers)
tree = html.fromstring(page2.text)

bid = tree.xpath('//span[@id="domhandler:4.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:BID.resetComp:PREV"]/text()')[0].replace('\n', '').strip()
bid = float(bid.replace(',', '.'))
print 'bid: ', bid

ask = tree.xpath('//span[@id="domhandler:5.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:ASK.resetComp:PREV"]/text()')[0].replace('\n', '').strip()
ask = float(ask.replace(',', '.'))
print 'ask: ', ask

tdate = tree.xpath('//span[@id="domhandler:10.consumer:VALUE-2CCLASS.comp:ZERO.gt:ZERO.eq:ZERO.lt:ZERO.resetLt:ZERO.resetGt:ZERO.resetEq:ZERO.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:DATE_BID.resetComp:ZERO.valueFilter:formatDateBidLong"]/text()')[0].replace('\n', '').strip() + " " + tree.xpath('//span[@id="domhandler:11.consumer:VALUE-2CCLASS.comp:ZERO.gt:ZERO.eq:ZERO.lt:ZERO.resetLt:ZERO.resetGt:ZERO.resetEq:ZERO.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:TIME_BID.resetComp:ZERO.valueFilter:formatTimeBidLong"]/text()')[0].replace('\n', '').strip()
tdate = datetime.strptime(tdate, '%d.%m.%Y %H:%M:%S')
print 'date: ', tdate

sqlConn = sqlConnector()
c = sqlConn.conn.cursor()
try: 
	c.execute("""INSERT INTO funds("wkn", "Bid", "Ask", "Date") VALUES(%s,%s,%s,%s)""",("847101", float(bid), float(ask), tdate))
	sqlConn.conn.commit()
except psycopg2.IntegrityError: 
	print "quote already in DB Funds"
	

sqlConn.conn.close()