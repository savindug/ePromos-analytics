import mysql.connector
from mysql.connector import errorcode
import datetime
from src.config.database import mssql_connection
import re
import uuid

DB_NAME = 'product_matching'
db = mssql_connection()
cursor = db.cursor()


def create_db():
    cursor.execute("CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    # print("Database {} created!".format(DB_NAME))


def create_product_table(table_name):
    query = "CREATE TABLE IF NOT EXISTS " + table_name + " ( `id` int(11) NOT NULL AUTO_INCREMENT, `code` varchar(250) NOT NULL, `name` varchar(250) NOT NULL, `price` varchar(250) NOT NULL, `product_page` text NOT NULL, `img` text NOT NULL, `desc` text NOT NULL, `created` timestamp not null default current_timestamp on update current_timestamp, PRIMARY KEY (`id`) ) ENGINE=InnoDB "

    try:
        # print("Creating table ({}) ".format(table_name), end="")
        cursor.execute(query)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Already Exists")
        else:
            print(err.msg)


def insert_product(product_no, product_name, product_price, product_page_url, product_img, product_desc_list, category,
                   size, page_no, position, conn):
    query = "INSERT INTO [product_matching].[4imprint_products] ([code],[name],[price],[product_page],[img],[desc],[category], [size], [page], [position]) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    data = (product_no, product_name, product_price, product_page_url, product_img, product_desc_list, category, size, page_no, position)
    try:
        print("Inserting Values into table 4imprint_products")
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)


def insert_discountmugs_category(group_category, sub_category, group_link, sub_link, conn):
    query = "INSERT INTO [product_matching].[discountmugs_categories] ([group_category] ,[sub_category], [group_category_link],[sub_category_link]) VALUES (?, ?, ?, ?)"
    data = (group_category, sub_category, group_link, sub_link,)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)


def insert_discountmugs_product(name, url, category, details, attributes, desc, pos, conn):
    query = "INSERT INTO [product_matching].[discountmugs_products] ([product_name],[product_page],[category],[product_details],[product_attributes],[product_desc],[listing_postion]) VALUES " \
            "(?, ?, ?, ?, ?, ?, ?)"
    data = (name, url, category, details, attributes, desc, pos)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)


def insert_discountmugs_product_price(name, url, print_method, qty, price, conn):
    query = "INSERT INTO [product_matching].[discountmugs_products_prices] ([product_name], [product_page], [print_method], [quantity], [price]) VALUES " \
            "(?, ?, ?, ?, ?)"
    data = (name, url, print_method, qty, price)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)

def fetch_discountmugs_distinct_product_urls(conn):
    c = conn.cursor()
    query = "SELECT distinct [product_page] FROM [product_matching].[product_matching].[discountmugs_products]  where created > '2022-08-20'"
    c.execute(query)
    result = c.fetchall()
    return [el[0] for el in result]

def fetch_discountmugs_categories(conn):
    c = conn.cursor()
    query = "SELECT [group_category], [sub_category],[group_category_link],[sub_category_link] FROM [product_matching].[product_matching].[discountmugs_categories]"
    c.execute(query)
    result = c.fetchall()
    return result


def fetch_epromos_products(categoryId):
    query = "SELECT name, productId, metaDescription, longDescription, vendorsKU, categoryId FROM [product_matching].[epromos_products] " \
            "where  categoryId = ?"
    cursor.execute(query, categoryId)

    result = cursor.fetchall()
    return result


def insert_ipromo_category(group_category, group_link, sub_category, sub_link, conn):
    query = "INSERT INTO [product_matching].[ipromo_categories] ([group_category] ,[group_category_link] ,[sub_category] ,[sub_category_link]) VALUES (?, ?, ?, ?)"
    data = (group_category, group_link, sub_category, sub_link)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)

def insert_ipromo_product(name, url, category, desc, attributes, pos, conn):
    query = "INSERT INTO [product_matching].[ipromo_products] ([product_name],[product_page],[category],[product_desc],[product_attributes],[listing_postion]) VALUES " \
            "(?, ?, ?, ?, ?, ?)"
    data = (name, url, category, desc, attributes, pos)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)

def insert_ipromo_product_price(name, url, set_up_charge, qty, price, conn):
    query = "INSERT INTO [product_matching].[ipromo_products_prices] ([product_name],[product_page],[set_up_charge],[quantity],[price]) VALUES " \
            "(?, ?, ?, ?, ?)"
    data = (name, url, set_up_charge, qty, price)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)

def insert_qualitylogoproducts_category(name, link, conn):
    query = "INSERT INTO [product_matching].[qualitylogoproducts_categories] ([category_name], [category_link]) VALUES (?, ?)"
    data = (name, link)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)

def insert_qualitylogoproducts_product(name, url, category, details, desc, pos, conn):
    query = "INSERT INTO [product_matching].[qualitylogoproducts_products] ([product_name],[product_page],[category],[product_details],[product_desc],[listing_postion]) VALUES " \
            "(?, ?, ?, ?, ?, ?)"
    data = (name, url, category, details, desc, pos)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)

def insert_qualitylogoproducts_product_price(name, url, set_up_charge, qty, price, conn):
    query = "INSERT INTO [product_matching].[qualitylogoproducts_products_prices] ([product_name],[product_page],[set_up_charge],[quantity],[price]) VALUES " \
            "(?, ?, ?, ?, ?)"
    data = (name, url, set_up_charge, qty, price)
    try:
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)

def fetch_qualitylogoproducts_categories(conn):
    c = conn.cursor()
    query = "SELECT [category_name], [category_link] FROM [product_matching].[qualitylogoproducts_categories] " \
            "where [category_name] not in (select distinct [category] from [product_matching].[qualitylogoproducts_products] )"
    c.execute(query)
    result = c.fetchall()
    return result

def fetch_ipromo_categories(conn):
    c = conn.cursor()
    query = "SELECT [group_category], [sub_category],[group_category_link],[sub_category_link] FROM [product_matching].[product_matching].[ipromo_categories]" \
            "where [sub_category] not in (select distinct [category] from [product_matching].[product_matching].[ipromo_products] )"
    c.execute(query)
    result = c.fetchall()
    return result

def fetch_ipromo_distinct_products(conn):
    c = conn.cursor()
    query = "select distinct [product_page] FROM [product_matching].[product_matching].[ipromo_products] where [product_page] not in " \
            "(select distinct [product_page] FROM [product_matching].[product_matching].[ipromo_products_prices] ) "
    c.execute(query)
    results = c.fetchall()
    return [result[0] for result in results]


def fetch_4imprint_products(conn, categoryId):
    c = conn.cursor()
    query = "SELECT * FROM [product_matching].[4imprint_products] where  category = ?"
    c.execute(query, categoryId)
    result = c.fetchall()
    return result


def fetch_product_matching_results(conn):
    c = conn.cursor()
    query = "SELECT distinct [4imprint_product_url] FROM [dbo].[product_matching_results]"
    c.execute(query)
    result = c.fetchall()
    return result


def get_product_materials(conn):
    c = conn.cursor()
    query = "SELECT materialId, materialName FROM [product_matching].[epromos_materials_table]"
    c.execute(query)
    result = c.fetchall()
    return result


def insert_parent_category(name, page, _type):
    query = "INSERT INTO [product_matching].[4imprint_categories] (catID, name, category_page, table_slug, type) VALUES(?, ?, ?, ?, ?)"
    data = ('cat_' + str(str(uuid.uuid4())), name, page, 'NULL', _type)
    try:
        print("Inserting Values into table 4imprint_categories")
        cursor.execute(query, data)
        db.commit()
    except mysql.connector.Error as err:
        print(err.msg)


def insert_sub_category(name, parent, page):
    query = "INSERT INTO [product_matching].[4imprint_sub_categories] (catID, parent_category, name, category_page) VALUES(?, ?, ?, ?)"
    data = ('sub_' + str(uuid.uuid4()), parent, name, page)
    try:
        print("Inserting Values into table 4imprint_sub_categories")
        cursor.execute(query, data)
        db.commit()
    except mysql.connector.Error as err:
        print(err.msg)


def insert_product_matching_results(productId, productName, vendorsKU, venderName, imprint_product_url,
                                    product_name_matching, product_material_matching, product_desc_matching,
                                    product_keyword_matching, conn):
    query = "INSERT INTO [dbo].[product_matching_results] ([epromos_productId],[epromos_productName],[vendorsKU],[venderName],[4imprint_product_url], [product_name_matching], [product_material_matching], [product_desc_matching], [product_keyword_matching])" \
            " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    data = (productId, productName, vendorsKU, venderName, imprint_product_url, product_name_matching,
            product_material_matching, product_desc_matching, product_keyword_matching)
    try:
        print("Inserting Values into table product_matching_results")
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)


def insert_4imprint_products_prices(sku, name, url, entryType, order, value, setupCharge, setupDesc, priceBreakCount,
                                    conn):
    query = "INSERT INTO [product_matching].[4imprint_products_prices] ([sku],[name],[url],[entryType],[order],[value],[setupCharge],[setupDesc],[priceBreakCount]) " \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    data = (sku, name, url, entryType, order, value, setupCharge, setupDesc, priceBreakCount)
    try:
        print("Inserting Values into table 4imprint_products_prices")
        conn.cursor().execute(query, data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err.msg)


def create_product_tables():
    query = "SELECT name FROM [product_matching].[4imprint_categories]"
    cursor.execute(query)
    result = cursor.fetchall()

    for res in result:
        create_product_table(res[1])


def get_table_by_category(category):
    query = "SELECT name FROM [product_matching].[4imprint_categories] where name = ?"
    data = (category,)
    cursor.execute(query, data)
    return cursor.fetchall()


def get_all_sub_categories():
    query = (
        "SELECT id, name, category_page FROM [product_matching].[product_matching].[4imprint_sub_categories]")
    cursor.execute(query)
    return cursor.fetchall()

# create_db()
# create_product_tables()
# create_product_table('4imprint_products')

# for el in get_product_materials():
#     print(f"{el}")

# insert_product_matching_results(8822039, 'productName', 'vendorsKU', 'venderName', 'imprint_product_url', 'product_name_matching', 'product_material_matching', 'product_desc_matching', 'product_keyword_matching', mssql_connection())
