from scrapers.NahkaufScraper import NahkaufScraper
from scrapers.NahkaufSel import NKScraperSel

#NH_offers = NahkaufScraper.scrape_for_offers('https://www.nahkauf.de/angebote-im-markt')
#print(NH_offers)
NKScraperSel.scrape_offers()
