from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://www.nahkauf.de/angebote-im-markt').text
soup = BeautifulSoup(html_text, 'lxml')

offers = soup.find_all('div', class_='offer-detail')
#todo: get all offer_details and loop
for offer in offers:
    offer_category = offer.find('h3', class_='offer-detail__headline').text
    print(offer_category + ':')

    products = offer.find_all('article', class_='product swiper-slide')
    for product in products:
        product_name = product.find('h3', class_='product__name').text.replace(' ', '').replace('\n', '')
        product_price = product.find('p', class_='product__price').text.replace(' ', '').replace('\n', '')
        print(product_name + ", " + product_price)

    print()


#offer_category = offer_table.find('h3', class_='offer-detail__headline').text
#print(offer_category)
# for every article do:

#product = offer_table.find('article', class_='product swiper-slide')

#product_name = product.find('h3', class_='product__name').text.replace(' ', '').replace('\n', '')
#product_price = product.find('p', class_='product__price').text.replace(' ', '').replace('\n', '')

#output = product_name + ", " + product_price
#print(output)

#offer_category = offer_table.find('h3', class_='offer-detail__headline').text

