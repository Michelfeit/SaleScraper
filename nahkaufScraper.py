from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.nahkauf.de/angebote-im-markt')
soup = BeautifulSoup(html_text, 'lxml')
