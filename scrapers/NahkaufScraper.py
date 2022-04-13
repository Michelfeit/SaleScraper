from bs4 import BeautifulSoup
import requests


class NahkaufScraper:

    target_path = 'target/Nahkauf.txt'

    @staticmethod
    def scrape_for_offers(url):
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        categories = NahkaufScraper.get_categories(soup)

        NahkaufScraper.create_offer_file(soup)
        NahkaufScraper.offers_to_string(soup)

        return categories

    @staticmethod
    def get_categories(soup):
        category_dict = {}
        offers = soup.find_all('div', class_='offer-detail')
        for offer in offers:
            offer_category = offer.find('h3', class_='offer-detail__headline').text
            category_dict[offer_category] = []
            products = offer.find_all('article', class_='product swiper-slide')
            for product in products:
                product_name = product.find('h3', class_='product__name').text.replace(' ', '').replace('\n', '')
                product_price = product.find('p', class_='product__price').text.replace(' ', '').replace('\n', '')
                product_dict = { product_name : product_price}
                category_dict[offer_category].append(product_dict)
        return category_dict

    @staticmethod
    def create_offer_file(soup):
        print("creating overview file at:" + NahkaufScraper.target_path)
        categories = NahkaufScraper.get_categories(soup)
        with open(NahkaufScraper.target_path, 'w', encoding="utf-8") as f:
            for category in categories:
                f.write(category + ':' + '\n')
                for product in categories.get(category):
                    for key in product:
                        f.write("{}, {}\n".format(key, product.get(key)))
                f.write('\n')

    @staticmethod
    def offers_to_string(soup):
        categories = NahkaufScraper.get_categories(soup)
        for category in categories:
            print(category + ':')
            for product in categories.get(category):
                for key in product:
                    print("{}, {}".format(key, product.get(key)))
            print()