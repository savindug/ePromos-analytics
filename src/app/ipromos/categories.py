from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from src.config.database import mssql_connection
from src.modules.database.dbQuaries import insert_discountmugs_category, insert_ipromo_category

website_url = 'https://www.ipromo.com'


def get_request(uri):
    ua = UserAgent()
    userAgent = ua.random
    return Request(uri, headers={'User-Agent': userAgent})


def extract_product_categories(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    conn = mssql_connection()

    categories_list = []

    category_wrappers = soup.find_all('div', class_="promotion-details")

    for category_wrapper in category_wrappers:

        sub_categories_li = category_wrapper.find_all('li')

        main_category_name = category_wrapper.find('h3').text.strip()

        try:
            main_category_link = sub_categories_li[-1].find('a')['href']
            sub_categories = find_sub_categories(main_category_link)

            for sub_category in sub_categories:

                # categories_list.append({
                #     "main_category_name": main_category_name,
                #     "main_category_link": website_url + main_category_link,
                #     "sub_category_name": sub_category["name"],
                #     "sub_category_link": sub_category["link"]
                # })

                insert_ipromo_category(main_category_name, website_url + main_category_link, sub_category["name"], sub_category["link"], conn)

        except Exception as e:
            print(e)


    # print(categories_list)


def find_sub_categories(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    sub_category_links = []

    try:
        sub_wrappers = soup.find_all('div', class_="subcategories-img")

        for sub_wrapper in sub_wrappers:
            sub_category_name = sub_wrapper.find('a').text.strip()
            sub_category_link = sub_wrapper.find('a')['href']
            sub_category_links.append({
                "name": sub_category_name,
                "link": sub_category_link
            })
    except Exception as e:
        print(e)

    return sub_category_links


if __name__ == '__main__':
    extract_product_categories('/all-promotional-items')

    # print(find_sub_categories('/group-category/drinkware/'))
