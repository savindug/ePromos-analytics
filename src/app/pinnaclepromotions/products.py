import json
import re
import time
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

from src.config.database import mssql_connection
from src.modules.database.dbQuaries import insert_discountmugs_product_price, insert_qualitylogoproducts_product, \
    insert_qualitylogoproducts_product_price

website_url = 'https://www.qualitylogoproducts.com'


def get_request(uri):
    ua = UserAgent()
    userAgent = ua.random
    return Request(uri, headers={'User-Agent': userAgent})


def get_next_page(soup):
    pages_wrapper = soup.find('ul', class_="pages-items")

    try:
        pages_wrapper.find('li', class_="pages-item-next")

        return True

    except Exception as e:
        return False


def extract_product_category(pageUrl, page_no, category, limit):
    while True:
        req = get_request(f"{pageUrl}?p={page_no}&product_list_limit={limit}")
        html_content = urlopen(req).read()
        soup = BeautifulSoup(html_content, 'lxml')

        if get_next_page(soup):
            extract_product_listing(soup, page_no, category)
            page_no = page_no + 1

        else:
            break


def extract_product_prices(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    print(f"extracting product: {pageUrl}")

    print_methods = []

    conn = mssql_connection()

    try:
        product_name = soup.find('section', class_="detail-product-code").find('h1').text.strip()

        product_tab = soup.find('div', class_="product-tab")

        print_methods_wrap = product_tab.find('ul', class_="nav-tabs1").find_all('li')

        print_methods = [ele.text.strip() for ele in print_methods_wrap]

        table_wrappers = product_tab.find_all('div', class_="tab-pane")

        for tbl_id, table_wrapper in enumerate(table_wrappers):
            tables = table_wrapper.find_all('table')

            table = tables[1]

            rows = table.find_all('tr')

            try:
                for row in rows:
                    tbl_rows = row.find('td', class_="moveable").find_all('tr')
                    qty = []
                    prices = []

                    for ix, tbl_row in enumerate(tbl_rows):
                        cols = tbl_row.find_all('td')
                        if ix == 0:
                            qty = [ele.text.strip().split(' ')[0] for ele in cols]
                        elif ix == 1:
                            prices = [ele.text.strip().split(' ')[0] for ele in cols]

                    # print(f"qty: {qty}")
                    # print(f"prices: {prices}")

                    for ix, price in enumerate(prices):
                        # price_qty = {
                        #     'method': print_methods[tbl_id],
                        #     'qty': qty[ix],
                        #     'price': price.split('\n')[-1]
                        # }

                        # print(price_qty)

                        insert_discountmugs_product_price(product_name, pageUrl, print_methods[tbl_id], qty[ix],
                                                          price.split('\n')[-1],
                                                          conn)

            except Exception as e:
                pass
    except Exception as e:
        print(e)

    # print(product_data)


def extract_product_listing(soup, page_no, category):
    # pageUrl = f"{pageUrl}?p={page_no}&product_list_limit={limit}"
    # req = get_request(pageUrl)
    # html_content = urlopen(req).read()
    # soup = BeautifulSoup(html_content, 'lxml')

    print(f"page_no: {page_no}")

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
    except Exception as e:
        print(e)

    for product in products_list:
        print(product)
        # extract_product_page(product["product_link"], product["category"],
        #                      {"page_no": product["page_no"], "listing_pos": product["listing_pos"]})

    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     return executor.map(execute_product_scrape, products_list)


def execute_product_scrape(product):
    extract_product_page(product["product_link"], product["category"],
                         {"page_no": product["page_no"], "listing_pos": product["listing_pos"]})


def extract_product_page(pageUrl, category, pos):
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

    conn = mssql_connection()

    print(f"extracting product on {pageUrl}")

    try:

        product_name = soup.find('h1', class_="page-title").text.strip()

        product_details = []

        product_desc = ""

        try:

            product_desc = soup.find('div', class_="description").find('div', class_="value").text.strip()


        except Exception as e:
            print(e)

        try:
            product_details_points = soup.find('table', id="product-attribute-specs-table").find_all('tr')

            for row in product_details_points:
                key = row.find('th').text.strip()
                value = row.find('td').text.strip()

                product_details.append({
                    key: value
                })
        except Exception as e:
            print(e)

        print(f"product_name: {product_name}, product_desc: {product_desc}\nproduct_details: {product_details}")


        try:

            qtys = []

            prices = []

            price_table = soup.find('div', class_="tier-price-options").find('table')

            price_table_rows = price_table.find_all('tr')

            for ix, row in enumerate(price_table_rows):

                if ix == 0:
                    for itm in row.find_all('td', class_="option-item"):
                        qtys.append(itm.text.strip())

                if ix == 1:
                    for itm in row.find_all('td', class_="option-item"):
                        prices.append(itm.text.strip())

            for i, qty in enumerate(qtys):
                print(f"qty: {qty}, price: {prices[i]}")
                # insert_qualitylogoproducts_product_price(product_name, pageUrl, 0, qty, price, conn)

        except Exception as e:
            print(e)

    except Exception as e:
        print(e)

    # try:
    #     insert_qualitylogoproducts_product(product_name, pageUrl, category, product_details,
    #                                        product_desc, json.dumps(pos), conn)
    # except Exception as e:
    #     print(e)

    driver.quit()


if __name__ == '__main__':
    # extract_product_category('https://www.qualitylogoproducts.com/drinkware-barware.htm?page=54',
    #                          'Custom Drinkware & Personalized Drinking Glasses')
    # extract_product_page(
    #     'https://www.qualitylogoproducts.com/openers/waiters-corkscrew-wine-bottle-opener.htm', 'Custom Drinkware & Personalized Drinking Glasses', 1)

    # extract_product_prices('https://www.discountmugs.com/product/exp07-2oz-executive-engraved-espresso-cups/')
    # print(find_sub_categories('/group-category/drinkware/'))

    # extract_product_category('https://www.pinnaclepromotions.com/custom-promotional-brands/nike.html', 1,
    #                          'custom-promotional-items', 72)

    extract_product_page('https://www.pinnaclepromotions.com/dri-fit-stretch-1-2-zip-cover-up.html', 'cat', 1)
