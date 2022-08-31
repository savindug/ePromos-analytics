import os
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC

from src.modules.database.dbServices import *

website_url = 'https://www.4imprint.com'


def get_request(uri):
    ua = UserAgent()
    print(ua.random)
    return Request(uri, headers={'User-Agent': ua.random})


def get_paginated_pages(pageUrl, category):
    try:
        req = get_request(pageUrl)
        html_content = urlopen(req).read()
        soup = BeautifulSoup(html_content, 'lxml')

        paging_links = soup.find('nav', class_="pagingLinks").ol

        paginations = paging_links.find_all('li')

        page_length = int(paginations[-2].text)

        # find_products(pageUrl + "?page=1")

        page_urls = []

        for x in range(1, (page_length + 1)):
            # thread.start_new_thread(find_products, (pageUrl + "?page=" + str(x)))
            # threading.Thread(target=find_products,
            #                  args=(pageUrl + "?page=" + str(x), category,)).start()
            # find_products(pageUrl + "?page=" + str(x), category)

            page_urls.append((pageUrl + "?page=" + str(x), category, x))

        with ThreadPoolExecutor(max_workers=page_length) as executor:
            return executor.map(exe_find_products, page_urls)
    except Exception as ex:
        print(f"Exception in get_paginated_pages: {ex}")
        find_products(pageUrl, category, 1)


def exe_find_products(url):
    find_products(url[0], url[1], url[2])


def find_products(pageUrl, category, page_no):
    try:
        connection = mssql_connection()
        req = get_request(pageUrl)
        html_content = urlopen(req).read()
        soup = BeautifulSoup(html_content, 'lxml')

        print(f'Finding products on {website_url + pageUrl}')

        productClass = "productListItem"

        productList = soup.find_all('div', class_=productClass)
        print(f'{len(productList)} products found ')
        for count, product in enumerate(productList):
            product_name = product.find('h3', class_="itemName").text
            product_page_url = product.find('a')['href']
            product_desc_list, product_no = get_more_details(product_page_url)
            product_price = product.find('p', class_="itemPrice").text
            product_img = ''
            if product.find('img', class_="responsiveImg").has_attr('src'):
                product_img = 'https:' + product.find('img', class_="responsiveImg")['src']
            elif product.find('img', class_="responsiveImg").has_attr('data-src'):
                product_img = 'https:' + product.find('img', class_="responsiveImg")['data-src']

            print_product(count + 1, product_no.split()[1][1:], product_name, product_price, product_page_url,
                          product_img,
                          product_desc_list,
                          category, page_no, connection)
    except Exception as ex:
        print(f"Exception in find_products: {ex}")


def print_product(count, product_no, product_name, product_price, product_page_url, product_img, product_desc_list,
                  category, page_no,
                  conn):
    size = "NULL"
    formatted_desc = ''
    # print(f'product_no: {product_no.strip()} ')
    # print(f'product_name: {product_name.strip()} ')
    # print(f'product_price: {product_price.strip()}')
    # print(f'More Info: {website_url + product_page_url} ')
    # print(f'product_img: {product_img} ')
    # print(f'product_desc: ')

    ozs = ["oz", "oz."]
    words = product_name.strip().lower().split()

    for oz in ozs:
        if oz in words[1:]:
            size = words[words.index(oz) - 1] + " oz"
            # print(f"product_size: {size}")

    for desc in product_desc_list:
        # print(f'\t* {desc.text.strip()}')
        formatted_desc = formatted_desc + ' ' + desc.text.strip()
    # print(f'\t*{formatted_desc}')
    add_product(product_no.strip(), product_name.strip(), product_price.strip(), website_url + product_page_url,
                product_img.strip(), formatted_desc, category, size, page_no, count, conn)


def get_more_details(product):
    req = get_request(website_url + product)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    product_no = "NULL"
    product_desc_list = "None"

    try:
        product_content = soup.find('main', id="mainContent")

        product_no = product_content.find('p', class_="prodNumber").text

        product_desc = product_content.find('section', class_="prodDetails").ul
        product_desc_list = product_desc.find_all('li')

    except Exception as ex:
        print(f"Exception in get_more_details: {ex}")

    return product_desc_list, product_no


def get_product_reviews(url):
    ua = UserAgent(verify_ssl=False)
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
    print(f'userAgent: {userAgent}, product: {url}')

    dir_path = os.path.dirname(os.path.realpath(__file__))
    chrome_driver = os.path.join(dir_path, '../../drivers/chromedriver.exe')
    # fire_fox_driver = dir_path + '/drivers/geckodriver.exe'
    os.environ['webdriver.chrome.driver'] = chrome_driver

    driver = webdriver.Chrome(options=options, executable_path=chrome_driver)

    driver.get(url)

    driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
    driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
    driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)

    try:
        ui.WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@id,  'ReviewsContainer')]"))
        )
    except Exception as e:
        driver.quit()
        insert_4imprint_product_review(url, 0, mssql_connection())
        return

    html = driver.execute_script("return document.documentElement.outerHTML")

    soup = BeautifulSoup(html, 'lxml')

    review_count = 0
    #
    # print(str(soup))
    driver.quit()

    try:
        reviewsContainer = soup.find('div', id="ReviewsContainer")

        review_container = reviewsContainer.find('div', class_="c-md-5 c-xs-half")

        review_count_text = review_container.find_all('p')[1].text

        review_count = ''.join([x for x in review_count_text.strip() if x.isdigit()])[2:]

        print(f"product: {url}, review_count: {review_count}")

    except Exception as ex:
        print(f"product: {url}, Exception in: {ex}")

    insert_4imprint_product_review(url, review_count, mssql_connection())

    return review_count


def fetch_category_products():
    sub_categories_list = fetch_all_sub_categories()

    for sub_category in sub_categories_list:
        # print(f"{sub_category}")
        get_paginated_pages(sub_category[3])


def extract_product_prices(product, conn):
    print(product)

    table_classes = ['marginBtm5', 'fullWidth']

    try:
        req = get_request(product)
        html_content = urlopen(req).read()
        soup = BeautifulSoup(html_content, 'lxml')

        product_content = soup.find('main', id="mainContent")

        product_no = product_content.find('p', class_="prodNumber").text

        product_name = soup.find('h1', class_="prodName").text

        formatted_desc = ""

        set_up_charge = "0"

        try:
            product_desc = product_content.find('section', id="detailsPanel")
            product_desc_list = product_desc.find_all('li')

            for desc in product_desc_list:
                formatted_desc = formatted_desc + ' ' + desc.text.strip()

            words = formatted_desc.strip().lower().split()
            print(words)
            if "set-up" in words[1:]:
                set_up_charge = words[words.index("set-up") + 3]
                print(f"set_up_charge: {set_up_charge}")
        except Exception as e:
            print("Exception in set_up_charge " + e)

        try:
            data = []

            table = soup.find('table', class_=table_classes)

            table_body = table.find('tbody')

            quantity_price = []

            rows = table_body.find_all('tr')

            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data.append([ele for ele in cols if ele])

            for i, quantity in enumerate(data[0]):
                quantity_price.append({"quantity": quantity, "price": data[1][i]})

            for x, q_p in enumerate(quantity_price):
                print(
                    f"url: {product}, productName: {product_name}, ProductSKU: {product_no.split()[1][1:]}, EntryType: qtyLevel, Order: {x + 1}, Value: {q_p['quantity']}, setupCharge: {''.join([x for x in set_up_charge if x.isdigit()])}")

                insert_4imprint_products_prices(product_no.split()[1][1:], product_name, product, "qtyLevel", x + 1,
                                                q_p['quantity'], ''.join([x for x in set_up_charge if x.isdigit()]),
                                                "set-up charge", 0, conn)

                print(
                    f"url: {product}, productName: {product_name}, ProductSKU: {product_no.split()[1][1:]}, EntryType: specialPrice, Order: {x + 1}, Value: {'$'.join([x for x in q_p['price'] if x.isdigit()])}, setupCharge: {''.join([x for x in set_up_charge if x.isdigit()])}")

                insert_4imprint_products_prices(product_no.split()[1][1:], product_name, product, "specialPrice", x + 1,
                                                q_p['price'], ''.join([x for x in set_up_charge if x.isdigit()]),
                                                "set-up charge", 0, conn)
        except Exception as e:
            print(" Exception in quantity_price " + e)

    except Exception as ex:
        print(f"Exception in extract_product_prices: {ex}")


def chunks(lst, s):
    n = round(len(lst) / s)
    res_arr = ()
    for i in range(0, len(lst), n):
        res_arr += (lst[i:i + n],)
    return res_arr


def execute_extraction(chunk):
    conn = mssql_connection()

    for url in chunk:
        extract_product_prices(url[0], conn)


def get_4imprint_products_prices():
    urls = fetch_product_matching_results(mssql_connection())

    arr_chunks = chunks(urls, 1)

    for chunk in arr_chunks:
        threading.Thread(target=execute_extraction, args=(chunk,)).start()


if __name__ == '__main__':
    # /tag/92/outerwear

    categories = [(546, 'https://www.4imprint.com/tag/115/travel-mugs'),
                  (548, 'https://www.4imprint.com/tag/110/ceramic-mugs'),
                  (554, 'https://www.4imprint.com/tag/7048/camp-mugs')]

    # search_key = input("Please Enter Search key: ")
    # if len(search_key) > 0:
    #     get_paginated_pages(search_key, 535)
    # else:
    #     print('Invalid Search Key')

    # for cat in categories:
    #     get_paginated_pages(cat[1], cat[0])

    # get_paginated_pages('https://www.4imprint.com/tag/7048/camp-mugs', 554)

    # fetch_category_products()
    # get_4imprint_products_prices()
