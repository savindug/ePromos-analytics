from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from src.modules.database.dbServices import *

website_url = 'https://www.4imprint.com'

all_category_wrapper_class = "floatRight c-md-10 c-sm-quarter-4 c-xs-full"
category_type_class = "textBlue textsemibold marginBtm15 paddingTop10 text25 borderTopMdGray"
category_wrapper_class = "displayFlex flexSameHeight flexSpaceBetween"
category_list_class = "c-xs-half c-sm-quarter-1 marginBtm40"
parent_category_class = "text16 textsemibold marginBtm10 bkgdLtGray padding10"


def get_request(uri):
    return Request(website_url + uri, headers={'User-Agent': 'Mozilla/5.0'})


def find_categories(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    print(f'Finding categories on {website_url + pageUrl}')

    all_category_wrapper = soup.find('div', class_=all_category_wrapper_class)

    category_types = all_category_wrapper.find_all('h2', class_=category_type_class)

    categories_wrapper = all_category_wrapper.find_all('div', class_=category_wrapper_class)

    for id, category_wrapper in enumerate(categories_wrapper):
        category_list = category_wrapper.find_all('div', class_=category_list_class)

        for category in category_list:
        # category = category_list[0]
            parent_category = category.find(attrs={'class': parent_category_class})
            parent_category_page = parent_category.find('a')['href']
            parent_category_type = category_types[id].text
            sub_categories_wrapper = category.find('ul')
            sub_categories_list = sub_categories_wrapper.find_all('li')

            print_parent_category(parent_category.text, website_url + parent_category_page, parent_category_type)

            for sub_category in sub_categories_list:
                sub_category_name = sub_category.find('a').text
                sub_category_page = sub_category.find('a')['href']
                print_sub_category(sub_category_name, website_url + sub_category_page, parent_category.text)

    return 0


def print_parent_category(name, page, _type):
    print(f'parent_name: {name.strip()} ')
    print(f'parent_page: {page.strip()}')
    print(f'parent_type: {_type.strip()} ')
    add_parent_category(name.strip(), page.strip(), _type.strip())


def print_sub_category(name, page, parent):
    print("\n")
    print(f'\tsub_name: {name.strip()} ')
    print(f'\tsub_page: {page.strip()}')
    print(f"\tparent_category: {parent.strip()}")
    add_sub_category(name.strip(), parent.strip(), page.strip())


# if __name__ == '__main__':
#     # /tag/92/outerwear
#     search_key = "/allproductcategories"
#     find_categories(search_key)
