from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from src.config.database import mssql_connection
from src.modules.database.dbQuaries import insert_discountmugs_category

website_url = 'https://www.discountmugs.com'

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

    category_wrappers = soup.find_all('div', class_ = "col-lg-3 col-sm-6 col-12 px-2")

    for category_wrapper in category_wrappers:
        main_category_link =  category_wrapper.find('a')['href']
        sub_categories = find_sub_categories(main_category_link)

        for sub_category in sub_categories:
            insert_discountmugs_category(main_category_link.split('/')[-2], sub_category["name"], website_url + main_category_link, sub_category["link"], conn)
            categories_list.append({
                "main_category": website_url + main_category_link,
                "sub_category": sub_category["link"]
            })

    print(categories_list)


def find_sub_categories(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    sub_category_links = []

    try:
        sub_wrappers = soup.find_all('div', class_="group_img position-relative text-right")

        for sub_wrapper in sub_wrappers:
            sub_category_name = sub_wrapper.find('div', class_="group_banner_title position-absolute w-50 text-left").text.strip()
            sub_category_link = sub_wrapper.find('a')['href']
            sub_category_links.append({
                "name": sub_category_name,
                "link": sub_category_link
            })
    except Exception as e:
        print(e)


    return sub_category_links


if __name__ == '__main__':
    extract_product_categories('/viewallcategories')

    # print(find_sub_categories('/group-category/drinkware/'))