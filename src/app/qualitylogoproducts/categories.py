from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

from src.app.qualitylogoproducts.categories_html import get_categories_html
from src.config.database import mssql_connection
from src.modules.database.dbQuaries import insert_discountmugs_category, insert_ipromo_category, \
    insert_qualitylogoproducts_category

website_url = 'https://www.qualitylogoproducts.com'


def get_request(uri):
    return Request(website_url + uri, headers={'User-Agent': 'Mozilla/5.0'})


def extract_product_categories(pageUrl):
    # ua = UserAgent()
    # userAgent = ua.random
    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    #
    # # options.add_argument("--headless")
    # options.add_argument('--disable-gpu')  # applicable to windows os only
    # options.add_argument('start-maximized')
    # options.add_argument("--disable-extensions")
    # options.add_argument('window-size=1920x1080');
    # options.add_argument(f'user-agent={userAgent}')
    #
    # driver = webdriver.Chrome(executable_path=r'C:\ChromeWebdriver\chromedriver.exe', options=options)
    #
    # driver.get(pageUrl)
    #
    # html_content = driver.execute_script("return document.documentElement.outerHTML")

    html_content = get_categories_html()

    soup = BeautifulSoup(html_content, 'lxml')

    conn = mssql_connection()

    categories_list = []

    # print(soup)

    categories_ul = soup.find('ul', class_="js-menu-ul")

    category_wrappers = categories_ul.find_all('li')

    for category_wrapper in category_wrappers:

        try:
            category_link = website_url +  category_wrapper.find('a')['href']
            category_name = category_wrapper.find('a')['data-title']

            insert_qualitylogoproducts_category(category_name, category_link, conn)

            print(f'{category_link}, {category_name}')
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
    extract_product_categories(website_url)

    # print(find_sub_categories('/group-category/drinkware/'))
