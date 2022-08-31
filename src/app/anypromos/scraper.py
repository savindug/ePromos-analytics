import json
from concurrent.futures.thread import ThreadPoolExecutor
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from src.modules.database.dbServices import *
from fake_useragent import UserAgent


def get_request(uri):
    ua = UserAgent()
    print(ua.random)
    return Request(uri, headers={'User-Agent': ua.random})


def scrape_product(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    data = soup.find_all('script', type='application/ld+json')

    for d in data:
        json_data = json.loads(d.string)
        if json_data['@type'] == 'Product':
            print(json.dumps(json_data, indent=4, sort_keys=True))

    return 0


def scrape_product(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    data = soup.find_all('script', type='application/ld+json')

    product_data_json = {}

    for d in data:
        json_data = json.loads(d.string)
        if json_data['@type'] == 'Product':
            product_data_json = json_data
            print(json.dumps(json_data, indent=4, sort_keys=True))

    return product_data_json


def scrape_sitemap(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    link_uls = soup.find_all('ul', class_='link-content')

    product_links = []

    for ul in link_uls:
        try:
            title = ul.find('li', class_='tilte')
            print(title.text)
        except Exception as e:
            print(e)

        try:
            link_sub_content = ul.find('li', class_='link-sub-content')
            links = link_sub_content.find_all('a')
            print(f'{len(links)} links found')
            for link in links:
                product_links.append(f'https://www.anypromo.com{link["href"]}')
                print(f'https://www.anypromo.com{link["href"]}')
        except Exception as e:
            print(e)

    return product_links


def scrape_product_listing(pageUrl):
    print(f'scrape product listing in {pageUrl}')
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    products_listing = []

    products_div = soup.find_all('div', class_='onsale-content')

    for product in products_div:
        try:
            product_info = product.find('div', class_="onsale_name")
            products_listing.append(
                (product_info.find('a')['title'], f'https://www.anypromo.com{product_info.find("a")["href"]}'))
        except Exception as e:
            print(e)

    print(products_listing)

    return products_listing


def handle_product_listing_pagination(pageUrl):
    req = get_request(pageUrl)
    html_content = urlopen(req).read()
    soup = BeautifulSoup(html_content, 'lxml')

    pagination = soup.find('ul', class_='pagination')
    pagination_pages = pagination.find_all('li')
    max_page = int(re.search(r'\d+', pagination_pages[-2].find('a')['href']).group())

    page_urls = []

    for x in range(1, max_page):
        page_urls.append(f"{pageUrl}?pagenum={str(x)}")

    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(scrape_product_listing, page_urls)


if __name__ == '__main__':
    search_key = "https://www.anypromo.com/apparel/business-wear/ash-city-core-365-mens-origin-performance-piqu-polo-all-p746563"
    # scrape_product(search_key)
    # scrape_sitemap('https://www.anypromo.com/sitemap')
    # scrape_product_listing('https://www.anypromo.com/apparel?pagenum=1')
    handle_product_listing_pagination('https://www.anypromo.com/apparel')
