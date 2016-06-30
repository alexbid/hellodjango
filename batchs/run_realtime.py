
#$1 can take:
#CRITICAL
#ERROR
#WARNING
#INFO
#DEBUG

import sys, os
addPath = os.path.realpath(__file__).replace('batchs/run_realtime.py','objects')
sys.path.append(addPath)

from common import *
import requests, datetime
from lxml import html

#import logging
#logging.basicConfig(level=sys.argv[1], format='%(asctime)s - %(levelname)s - %(message)s')
#logging.basicConfig(filename='logs_realtime.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome", "Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}

page2 = requests.get('https://www.boerse-stuttgart.de/de/boersenportal/wertpapiere-und-maerkte/fonds/factsheet/?ID_NOTATION=15314068', headers = headers)
tree = html.fromstring(page2.text)

bid0 = tree.xpath('//span[@id="domhandler:4.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:BID.resetComp:PREV"]/text()')
ask0 = tree.xpath('//span[@id="domhandler:5.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:ASK.resetComp:PREV"]/text()')
tdate0 = tree.xpath('//span[@id="domhandler:10.consumer:VALUE-2CCLASS.comp:ZERO.gt:ZERO.eq:ZERO.lt:ZERO.resetLt:ZERO.resetGt:ZERO.resetEq:ZERO.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:DATE_BID.resetComp:ZERO.valueFilter:formatDateBidLong"]/text()')
tdate1 = tree.xpath('//span[@id="domhandler:11.consumer:VALUE-2CCLASS.comp:ZERO.gt:ZERO.eq:ZERO.lt:ZERO.resetLt:ZERO.resetGt:ZERO.resetEq:ZERO.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:TIME_BID.resetComp:ZERO.valueFilter:formatTimeBidLong"]/text()')

if len(bid0) > 0: bid = bid0[0].replace('\n', '').strip()
else: bid = '-'
if len(ask0) > 0: ask = ask0[0].replace('\n', '').strip()
else:  ask = '-'
if (len(tdate0) > 0) and (len(tdate1) > 0): tdate = tdate0[0].replace('\n', '').strip() + " " + tdate1[0].replace('\n', '').strip()
else: tdate = '-'

#bid = tree.xpath('//span[@id="domhandler:4.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:BID.resetComp:PREV"]/text()')[0].replace('\n', '').strip()
#ask = tree.xpath('//span[@id="domhandler:5.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:ASK.resetComp:PREV"]/text()')[0].replace('\n', '').strip()
#tdate = tree.xpath('//span[@id="domhandler:10.consumer:VALUE-2CCLASS.comp:ZERO.gt:ZERO.eq:ZERO.lt:ZERO.resetLt:ZERO.resetGt:ZERO.resetEq:ZERO.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:DATE_BID.resetComp:ZERO.valueFilter:formatDateBidLong"]/text()')[0].replace('\n', '').strip() + " " + tree.xpath('//span[@id="domhandler:11.consumer:VALUE-2CCLASS.comp:ZERO.gt:ZERO.eq:ZERO.lt:ZERO.resetLt:ZERO.resetGt:ZERO.resetEq:ZERO.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:TIME_BID.resetComp:ZERO.valueFilter:formatTimeBidLong"]/text()')[0].replace('\n', '').strip()

if ('-' not in bid) and ('-' not in ask) and ('-' not in tdate):
    bid = float(bid.replace(',', '.'))
    ask = float(ask.replace(',', '.'))
    tdate = datetime.datetime.strptime(tdate, '%d.%m.%Y %H:%M:%S')

    logging.debug('bid %s', bid)
    logging.debug('ask %s', ask)
    logging.debug('date %s', tdate)

    c = conn.cursor()
    try:
        c.execute("""INSERT INTO funds("wkn", "Bid", "Ask", "Date") VALUES(%s,%s,%s,%s)""",("847101", float(bid), float(ask), tdate))
        conn.commit()
    except psycopg2.IntegrityError:
        logging.info('quote already in DB Funds %s %s %s', bid, ask, tdate)

    conn.close()
