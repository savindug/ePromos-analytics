import json
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from src.config.database import mssql_connection
from src.modules.database.dbQuaries import insert_discountmugs_category, insert_discountmugs_product, \
    insert_discountmugs_product_price

website_url = 'https://www.discountmugs.com'


def get_request(uri):
    ua = UserAgent()
    userAgent = ua.random
    return Request(uri, headers={'User-Agent': userAgent})


def get_pages(soup):
    pages_wrapper = soup.find('div', class_="pagination-holder-r")

    pages = []

    try:
        page_links = pages_wrapper.find_all('li')

        for page_link in page_links:
            if page_link.text.strip().isdigit():
                pages.append(page_link.text.strip())
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
        pages.append((f"{pageUrl}?pg={page}", page, category))

    with ThreadPoolExecutor(max_workers=1) as executor:
        return executor.map(execute_product_scrape, pages)


def execute_product_scrape(product):
    extract_product_listing(product[0], product[1], product[2])


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

                        insert_discountmugs_product_price(product_name, pageUrl, print_methods[tbl_id], qty[ix], price.split('\n')[-1],
                                                          conn)

            except Exception as e:
                pass
    except Exception as e:
        print(e)


    # print(product_data)


def extract_product_listing(pageUrl, page_no, category):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    try:
        products_list = []

        product_wrappers = soup.find_all('div', class_="prod-box")

        for ix, product_wrapper in enumerate(product_wrappers):
            _product = product_wrapper.find('span', class_="item-name").find('a')
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
        extract_product_page(product["product_link"], product["category"],
                             {"page_no": product["page_no"], "listing_pos": product["listing_pos"]})


def extract_product_page(pageUrl, category, pos):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    conn = mssql_connection()

    try:

        product_name = soup.find('section', class_="detail-product-code").find('h1').text.strip()

        product_details = ''

        product_desc = ""

        try:
            product_details_points = soup.find('section', class_="detail-bot-product-details-content").find_all('li')

            _descs = soup.find('div', class_="pr-description-holder").find_all('p')

            for _desc in _descs:
                product_desc = f"{product_desc} {_desc.text.strip()}"

            for product_details_point in product_details_points:
                if len(product_details) == 0:
                    product_details = {product_details_point.text.strip()}
                else:
                    product_details = f"{product_details} {product_details_point.text.strip()}"


        except Exception as e:
            print(e)

        print(f"{product_name}, {product_details}")

        product_data = []

        try:

            table = soup.find('table', class_="dm-specs-tab")

            rows = table.find_all('tr')

            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                product_data.append({
                    cols[0]: cols[1]
                })

        except Exception as e:
            print(e)

    except Exception as e:
        print(e)

    try:
        insert_discountmugs_product(product_name, pageUrl, category, product_details, json.dumps(product_data),
                                    product_desc, json.dumps(pos), conn)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    extract_product_category('https://www.discountmugs.com/category/custom-personalized-ceramic-coffee-mugs/', 'Plastic Cups')
    # extract_product_page(
    #     'https://www.discountmugs.com/product/7102-11-oz.-traditional-personalized-ceramic-coffee-mugs/')

    extract_product_prices('https://www.discountmugs.com/product/exp07-2oz-executive-engraved-espresso-cups/')
    # print(find_sub_categories('/group-category/drinkware/'))
