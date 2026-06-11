import psycopg2
from config.db_config import HOST, DATABASE, USER, PASSWORD, PORT

def get_connection():
    conn=psycopg2.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        port=PORT
    )
    return conn
