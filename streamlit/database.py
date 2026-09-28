import mysql.connector
import pandas as pd


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL@2026Strong",
        database="cart2"
    )


def run_query(query):
    conn = get_connection()

    try:
        df = pd.read_sql(query, conn)
        return df

    finally:
        conn.close()