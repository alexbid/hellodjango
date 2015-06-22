

from lxml import html
import requests

page = requests.get('https://www.boerse-stuttgart.de/de/boersenportal/factsheets/letzte-taxierungen/?ID_NOTATION=15314068')
tree = html.fromstring(page.text)

#bid = tree.xpath('//td[@class="nowrap"]/text()')
#print 'bid: ', bid

#ask = tree.xpath('//td[@class="right nowrap"]/text()')
#print 'ask: ', ask

page2 = requests.get('https://www.boerse-stuttgart.de/de/boersenportal/wertpapiere-und-maerkte/fonds/factsheet/?ID_NOTATION=15314068')
tree = html.fromstring(page2.text)

bid = tree.xpath('//span[@id="domhandler:4.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:BID.resetComp:PREV"]/text()')
print 'bid: ', bid[0].replace('\n', '').strip()
ask = tree.xpath('//span[@id="domhandler:5.consumer:VALUE-2CCLASS.comp:PREV.gt:push-2Dup.eq:.lt:push-2Ddown.resetLt:.resetGt:.resetEq:.mdgObj:prices-2Fquote-3FVERSION-3D2-26ID_NOTATION-3D15314068-26ID_QUALITY_PRICE-3D4.attr:ASK.resetComp:PREV"]/text()')
print 'ask: ', ask[0].replace('\n', '').strip()
