import psycopg2
from psycopg2 import Error
from config import DB_CONFIG
import os

def get_connection():
    try:
        if os.getenv("DATABASE_URL"):
            conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        else:
            conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f" Connection error: {e}")
        return None


def close_connection(conn):
    if conn is not None:
        try:
            conn.close()
        except Exception as e:
            print(f" Error closing connection: {e}")