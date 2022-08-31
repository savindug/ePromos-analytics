import json
import re
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from src.config.database import mssql_connection
from src.modules.database.dbQuaries import insert_discountmugs_product_price, insert_qualitylogoproducts_product, insert_qualitylogoproducts_product_price

website_url = 'https://www.qualitylogoproducts.com'


def get_request(uri):
    ua = UserAgent()
    userAgent = ua.random
    return Request(uri, headers={'User-Agent': userAgent})


def get_pages(soup):
    pages_wrapper = soup.find('ul', class_="js-pagination")

    next_pages_link = ''

    try:
        page_links = pages_wrapper.find_all('li')

        if page_links[-1].find('a')['href'] != '':
            next_pages_link = website_url + page_links[-1].find('a')['href']


    except Exception as e:
        pass

    return next_pages_link


def extract_product_category(pageUrl, category):
    pages = []

    pages_link = pageUrl

    while len(pages_link) > 0:
        req = get_request(pages_link)
        html_content = urlopen(req).read()
        soup = BeautifulSoup(html_content, 'lxml')

        extract_product_listing(soup, pages_link.split('?page=')[-1], category)
        pages.append(pages_link)

        pages_link = get_pages(soup)

    # print(pages)



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
    # req = get_request(pageUrl)
    # html_content = urlopen(req).read()
    # soup = BeautifulSoup(html_content, 'lxml')

    try:
        products_list = []

        product_wrappers = soup.find_all('article', class_="prod-box")

        for ix, product_wrapper in enumerate(product_wrappers):
            _product = product_wrapper.find_all('a', class_="prod-box__info-title")[1]
            product_name = _product.text.strip()
            product_link = website_url + _product['href']
            products_list.append({
                "product_name": product_name,
                "product_link": product_link,
                "category": category,
                "page_no": page_no,
                "listing_pos": ix + 1
            })
    except Exception as e:
        print(e)

    # for product in products_list:
    #     # print(product)
    #     extract_product_page(product["product_link"], product["category"],
    #                          {"page_no": product["page_no"], "listing_pos": product["listing_pos"]})

    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(execute_product_scrape, products_list)


def execute_product_scrape(product):
    extract_product_page(product["product_link"], product["category"],
                         {"page_no": product["page_no"], "listing_pos": product["listing_pos"]})


def extract_product_page(pageUrl, category, pos):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    conn = mssql_connection()

    print(f"extracting product on {pageUrl}")

    try:

        product_name = soup.find('section', class_="pdp-preview__right").find('header').text.strip()

        product_details = ''

        product_desc = ""

        try:

            product_desc = soup.find('div', class_="js-item-details-left").find('article').text.strip()


        except Exception as e:
            print(e)

        try:
            product_details_points = soup.find('section', class_="pdp-desc-list").find_all('li')

            for product_details_point in product_details_points:
                if len(product_details) == 0:
                    product_details = {product_details_point.text.strip()}
                else:
                    product_details = f"{product_details} {product_details_point.text.strip()}"


        except Exception as e:
            print(e)


        try:

          pricing_buttons = soup.find_all('button', class_="pdp-pricing__item")

          for button in pricing_buttons:
              price_attrs = button.find('p', class_="pdp-pricing-price").attrs
              qty_attrs = button.find('p', class_="pdp-pricing-qty").find_all('span')[-1].attrs

              qty = 0

              price = 0



              qty_attrs_keys = (*qty_attrs,)

              price_attrs_keys = (*price_attrs,)


              for k in qty_attrs_keys:
                  if "data-" in k:
                      qty = (qty_attrs.get(k))

              for k in price_attrs_keys:
                  if "data-" in k:
                      price = (price_attrs.get(k))

              insert_qualitylogoproducts_product_price(product_name, pageUrl, 0, qty, price, conn)

        except Exception as e:
            print(e)

    except Exception as e:
        print(e)

    try:
        insert_qualitylogoproducts_product(product_name, pageUrl, category, product_details,
                                    product_desc, json.dumps(pos), conn)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # extract_product_category('https://www.qualitylogoproducts.com/drinkware-barware.htm?page=54',
    #                          'Custom Drinkware & Personalized Drinking Glasses')
    extract_product_page(
        'https://www.qualitylogoproducts.com/openers/waiters-corkscrew-wine-bottle-opener.htm', 'Custom Drinkware & Personalized Drinking Glasses', 1)

    # extract_product_prices('https://www.discountmugs.com/product/exp07-2oz-executive-engraved-espresso-cups/')
    # print(find_sub_categories('/group-category/drinkware/'))
