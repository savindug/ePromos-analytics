from concurrent.futures.thread import ThreadPoolExecutor

from src.app.scrapping.categories_scrapping import *
from src.app.scrapping.products_scrapping import get_paginated_pages


def execute_product_scraping(category):
    get_paginated_pages(category[2], category[0])


def exe_threads(categories):
    with ThreadPoolExecutor(max_workers=5) as executor:
        return executor.map(execute_product_scraping, categories)


if __name__ == '__main__':
    # if find_categories("/allproductcategories") == 0:
    #     sub_categories = fetch_all_sub_categories()
    #
    #     for cat in sub_categories:
    #         if cat[0] == 507:
    #             execute_product_scraping(cat)
    #     # exe_threads(sub_categories)

    sub_categories = fetch_all_sub_categories()

    for cat in sub_categories:
        if cat[0] == 507:
            execute_product_scraping(cat)
