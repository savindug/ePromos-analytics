import json
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager

from src.config.database import mssql_connection
from src.init_web_driver import init_web_driver
from src.modules.database.dbQuaries import insert_discountmugs_category, insert_discountmugs_product, \
    insert_discountmugs_product_price, insert_ipromo_product, insert_ipromo_product_price

from selenium.webdriver.chrome.service import Service

from selenium import webdriver

website_url = 'https://www.ipromo.com'


def get_request(uri):
    ua = UserAgent()
    userAgent = ua.random
    return Request(uri, headers={'User-Agent': userAgent})


def get_pages(soup):
    pages = ['1']

    try:
        pages_wrapper = soup.find('div', class_="pages")

        page_links = pages_wrapper.find_all('li')

        for page_link in page_links:
            page_no = page_link.text.strip().split(' ')[1]
            if page_no.isdigit():
                pages.append(page_no)

    except Exception as e:
        print(e)

    return pages


def extract_product_category(pageUrl, category):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    pages_links = get_pages(soup)

    pages = []

    for page in pages_links:
        pages.append((f"{pageUrl}?p={page}", page, category))

    # for page in pages:
    #     execute_product_scrape(page)

    with ThreadPoolExecutor(max_workers=len(pages)) as executor:
        return executor.map(execute_product_scrape, pages)


def execute_product_scrape(product):
    extract_product_listing(product[0], product[1], product[2])


def extract_product_prices(pageUrl):
    ua = UserAgent()
    userAgent = ua.random
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')

    options.add_argument("--headless")
    options.add_argument('--disable-gpu')  # applicable to windows os only
    options.add_argument('start-maximized')
    options.add_argument("--disable-extensions")
    options.add_argument('window-size=1920x1080');
    options.add_argument(f'user-agent={userAgent}')

    driver = webdriver.Chrome(executable_path=r'C:\ChromeWebdriver\chromedriver.exe', options=options)

    driver.get(pageUrl)

    html_content = driver.execute_script("return document.documentElement.outerHTML")

    soup = BeautifulSoup(html_content, 'lxml')

    print(f"extracting product: {pageUrl}")

    conn = mssql_connection()

    # time.sleep(3)

    try:

        product_name = soup.find('h1', class_="page-title").text.strip()

    except Exception as e:
        pass

    try:

        set_up_charge = soup.find('span', class_="setup-charge").find('span').text.strip()

    except Exception as e:
        print(e)

    try:

        table_prices = soup.find('table', class_="table-qty-price")

        qty_rows = table_prices.find('tr', class_="qty-row").find_all('td')
        price_rows = table_prices.find('tr', class_="price-row").find_all('td')

        for ix, qty in enumerate(qty_rows):
            insert_ipromo_product_price(product_name, pageUrl, set_up_charge, qty.text.strip(),
                                        price_rows[ix].text.strip(), conn)

    except Exception as e:
        print('prices not found')



    except Exception as e:
        print(e)

    driver.quit()


def extract_product_listing(pageUrl, page_no, category):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    try:
        products_list = []

        product_wrappers = soup.find_all('li', class_="product-item")

        for ix, product_wrapper in enumerate(product_wrappers):
            _product = product_wrapper.find('strong', class_="product-item-name").find('a')
            product_name = _product.text.strip()
            product_link = _product['href']
            products_list.append({
                "product_name": product_name,
                "product_link": product_link,
                "category": category,
                "page_no": page_no,
                "listing_pos": ix + 1
            })
        # print(products_list)
    except Exception as e:
        print(e)

    with ThreadPoolExecutor(max_workers=len(products_list)) as executor:
        return executor.map(run_extract_product_page, products_list)

    # for product in products_list:
    #     extract_product_page(product["product_link"], product["category"],
    #                          {"page_no": product["page_no"], "listing_pos": product["listing_pos"]})


def run_extract_product_page(product):
    extract_product_page(product["product_link"], product["category"],
                         {"page_no": product["page_no"], "listing_pos": product["listing_pos"]})


def extract_product_page(pageUrl, category, pos):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    conn = mssql_connection()

    try:

        product_name = soup.find('h1', class_="page-title").text.strip()

        print(f"extracting product: {product_name}")

        product_desc = ''

        try:
            product_desc = \
                soup.find('div', class_='description').find('div', class_="value").text.strip().split('Description')[-1]

        except Exception as e:
            print(e)

        product_data = []

        try:

            table = soup.find('table', class_="additional-attributes")

            rows = table.find_all('tr')

            for row in rows:
                key = row.find('th').text.strip()
                value = row.find('td').text.strip()

                product_data.append({
                    key: value
                })

        except Exception as e:
            print(e)



    except Exception as e:
        print(e)

    try:
        insert_ipromo_product(product_name, pageUrl, category, product_desc, json.dumps(product_data),
                              json.dumps(pos), conn)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # extract_product_category('https://www.discountmugs.com/category/custom-personalized-ceramic-coffee-mugs/')
    # extract_product_page(
    #     'https://www.discountmugs.com/product/7102-11-oz.-traditional-personalized-ceramic-coffee-mugs/')

    # extract_product_prices('https://www.discountmugs.com/product/exp07-2oz-executive-engraved-espresso-cups/')
    # print(find_sub_categories('/group-category/drinkware/'))

    # extract_product_category('https://www.ipromo.com/apparel/t-shirts.html', 'T-Shirts')

    # extract_product_page('https://www.ipromo.com/20-oz-vacuum-insulated-stainless-steel-tumbler.html', 'T-Shirts', 99)

    extract_product_prices('https://www.ipromo.com/under-armour-performance-locker-2-0-t-shirt-men.html')
