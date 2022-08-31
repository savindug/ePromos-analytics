from src.app.qualitylogoproducts.products import extract_product_category
from src.config.database import mssql_connection
from src.modules.database.dbQuaries import fetch_qualitylogoproducts_categories

conn = mssql_connection()

def scrape_products():
    categories = fetch_qualitylogoproducts_categories(conn)

    for category in categories:
        extract_product_category(category[1], category[0])


if __name__ == '__main__':
    scrape_products()