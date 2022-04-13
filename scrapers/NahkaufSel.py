import time

from ScraperLibrary.Product import Product
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from ScraperLibrary.ProgressBar import ProgressBar


_PATH = 'C:/Users/Miche/Documents/Repository/SaleScraper/webdrivers/chromedriver.exe'
NAHKAUF_WEB_ADDRESS = 'https://www.nahkauf.de/angebote-im-markt'
ZIP_AND_ADDRESS = '76133 Erzbergerstraße'

# for page navigation
COOKIE_BTN_ID = 'uc-btn-accept-banner'
SELECT_MARKET_TOP_RIGHT_XPATH = '/html/body/div[1]/div/header/div/div[3]/ul/li[2]/a/span'
SELECT_MARKET_POP_UP_XPATH = '/html/body/div[1]/section/div[2]/div[2]/div/button'
ZIP_INPUT_XPATH = '/html/body/div[1]/section/div[2]/div[3]/div/div/input'
SELECT_MARKET_AFTER_ZIP_XPATH = '/html/body/div[1]/section/div[2]/div[4]/div[2]/a'
PRODUCT_PAGE_NAVIGATOR_XPATH = '/html/body/div[1]/div/header/div/div[2]/nav/ul[1]/li[2]/a'


class NKScraperSel:
    @staticmethod
    def scrape_offers():
        # set to False when not debugging
        debug = False
        print('initializing webdriver...')
        driver = NKScraperSel._initialize_driver(debug)
        print('webdriver initialized.\n')
        driver.get(NAHKAUF_WEB_ADDRESS)
        print("navigating to product page...")
        NKScraperSel._navigate_to_offers(driver)
        print("navigation completed.\n")
        NKScraperSel._find_and_parse_offers(driver)
        time.sleep(500)

    @staticmethod
    def _initialize_driver(debug: bool) -> webdriver:
        chrome_options = Options()
        # Comment out for debugging.
        if not debug:
            # this line allows chrome to run in the background.
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(executable_path=_PATH, options=chrome_options)
        driver.maximize_window()
        return driver

    @staticmethod
    def _navigate_to_offers(driver):
        # i)    waiting for pop-up and accepting cookie policy
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.ID, COOKIE_BTN_ID))).click()
        ProgressBar.print_progress_bar(0, 5, prefix='Progress:', suffix='Complete', length=50, fill='#')
        # print('1/6')
        # ii)   clicking on 'select-market' in the top right corner
        driver.find_element(By.XPATH, SELECT_MARKET_TOP_RIGHT_XPATH).click()
        ProgressBar.print_progress_bar(1, 5, prefix='Progress:', suffix='Complete', length=50, fill='#')
        # print('2/6')
        # iii)  waiting for pop-up and clicking on 'select-market' button
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, SELECT_MARKET_POP_UP_XPATH))).click()
        ProgressBar.print_progress_bar(2, 5, prefix='Progress:', suffix='Complete', length=50, fill='#')
        # print('3/6')
        # iv)   waiting for search bar to appear and entering the zip code as well as the address
        input_space = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, ZIP_INPUT_XPATH)))
        input_space.send_keys(ZIP_AND_ADDRESS)
        input_space.send_keys(Keys.RETURN)
        ProgressBar.print_progress_bar(3, 5, prefix='Progress:', suffix='Complete', length=50, fill='#')
        # print('4/6')
        # v)    select correct market after entering zip
        time.sleep(0.5)
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, SELECT_MARKET_AFTER_ZIP_XPATH))).click()
        ProgressBar.print_progress_bar(4, 5, prefix='Progress:', suffix='Complete', length=50, fill='#')
        # print('5/6')
        # vi)  navigate to product page
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((
                By.XPATH, PRODUCT_PAGE_NAVIGATOR_XPATH))).click()
        ProgressBar.print_progress_bar(5, 5, prefix='Progress:', suffix='Complete', length=50, fill='#')
        # print('6/6')

    @staticmethod
    def _find_and_parse_offers(driver):
        # instantiate dictionary of categories
        category_dict = {}
        category_list = driver.find_elements(By.CLASS_NAME, 'offer-detail')
        for category in category_list:
            # get category name
            category_name = category.find_element(By.TAG_NAME, 'h3').text
            # add a new category to the list
            category_dict[category_name] = []
            print(category.find_element(By.TAG_NAME, 'h3').text)  # todo: logger

            # loop threw articles in each category
            offers = category.find_element(
                By.CLASS_NAME, 'offer-detail__slider').find_element(
                By.CLASS_NAME, 'offer-detail__wrapper').find_elements(
                By.TAG_NAME, 'article')
            for offer in offers:
                # get the img url of the product
                product_image_url = offer.find_element(
                    By.CLASS_NAME, 'product__image').find_element(
                    By.TAG_NAME, 'img').get_attribute('src')
                # print(product_image_url)  # todo: logger

                # get the name of the product
                product_name = offer.find_element(By.CLASS_NAME, 'product__infos').find_element(By.TAG_NAME, 'h3').text
                # print(product_name)  # todo: logger

                # get the object that encapsulates the price tag
                product_price_tag = offer.find_element(By.CLASS_NAME, 'product__price-label')
                # get the price of the product
                product_price = float(product_price_tag.find_element(
                    By.CLASS_NAME, 'product__price').text.replace('\n', ''))
                # print(product_price)  # todo: logger
                # get the discount of the product (either the percentage or the label 'Aktionspreis'
                discount_label = product_price_tag.find_element(By.CLASS_NAME, 'product__price-discount').text
                is_promotional = not str(discount_label)[0].isdigit()
                product_discount = 0
                if not is_promotional:
                    product_discount = float(discount_label[0:2])/100
                # print(product_discount)  # todo: logger
                product = Product(product_name, product_image_url, product_price,
                                  product_discount, is_promotional, '', '')
                print(product.str())
            print()  # todo: logger
