from concurrent.futures.thread import ThreadPoolExecutor

from src.app.ipromos.products import extract_product_category, extract_product_prices
from src.config.database import mssql_connection
from src.modules.database.dbQuaries import fetch_discountmugs_categories, fetch_discountmugs_distinct_product_urls, \
    fetch_ipromo_categories, fetch_ipromo_distinct_products

conn = mssql_connection()


def run(category):
    extract_product_category(category[3], category[1])


def scrape_products():
    categories = fetch_ipromo_categories(conn)

    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(run, categories)


def scrape_product_prices():
    products_list = fetch_ipromo_distinct_products(conn)

    with ThreadPoolExecutor(max_workers=10) as executor:
        return executor.map(extract_product_prices, products_list)


if __name__ == '__main__':
    scrape_product_prices()
