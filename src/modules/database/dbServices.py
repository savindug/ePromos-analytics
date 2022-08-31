from src.modules.database.dbQuaries import *


def add_product(product_no, product_name, product_price, product_page_url, product_img, product_desc_list, category, size, conn):
    insert_product(product_no, product_name, product_price, product_page_url, product_img, product_desc_list, category, size, conn)


def get_epromos_products(categoryId):
    return fetch_epromos_products(categoryId)


def get_4imprint_products(conn, categoryId):
    return fetch_4imprint_products(conn, categoryId)


def get_materials_list(conn):
    return get_product_materials(conn)


def add_parent_category(name, page, _type):
    insert_parent_category(name, page, _type)


def add_sub_category(name, parent, page):
    insert_sub_category(name, parent, page)


def add_matching_result(productId, productName, vendorsKU, venderName, imprint_product_url, product_name_matching, product_material_matching, product_desc_matching, product_keyword_matching, conn):
    insert_product_matching_results(productId, productName, vendorsKU, venderName, imprint_product_url, product_name_matching, product_material_matching, product_desc_matching, product_keyword_matching, conn)


def fetch_all_sub_categories():
    return get_all_sub_categories()
