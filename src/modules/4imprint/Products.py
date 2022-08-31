import mysql.connector
from mysql.connector import errorcode
from src.config.database import init_db_connection


class Product:
    def __init__(self, product_no, product_name, product_price, product_page_url, product_img, product_desc_list):
        self.product_no = product_no
        self.product_name = product_name
        self.product_price = product_price
        self.product_page_url = product_page_url
        self.product_img = product_img
        self.product_desc_list = product_desc_list
        self.conn = init_db_connection()

    def insert_product(self):
        query = "INSERT INTO `4imprint_products`(`code`, `name`, `price`, `product_page`, `img`, `desc`) VALUES(%s, %s, %s, %s, %s, %s)"
        data = (self.product_no, self.product_name, self.product_price, self.product_page_url, self.product_img, self.product_desc_list)
        try:
            print("Inserting Values into table 4imprint_products")
            self.conn.cursor.execute(query, data)
            self.conn.commit()
        except mysql.connector.Error as err:
            print(err.msg)