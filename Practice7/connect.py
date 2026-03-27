import psycopg2
from psycopg2 import Error
import config

def get_connection():
    try:
        conn = psycopg2.connect(**config.DB_CONFIG)
        return conn
    except Error as e:
        print(f"Ошибка подключения к PostgreSQL: {e}")
        return None

def close_connection(conn):
    if conn:
        conn.close()