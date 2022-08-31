import mysql.connector
import pyodbc
from decouple import config

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'product_matching'
}


def init_db_connection():
    return mysql.connector.connect(**db_config)


def mssql_connection():
    return pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=' + config('MSSQL_SERVER') + ';'
                          'Database=' + config('DB_NAME') + ';'
                          'Trusted_Connection=yes;')
