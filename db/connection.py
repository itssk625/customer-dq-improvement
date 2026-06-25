import psycopg2
#from config.db_config import HOST, DATABASE, USER, PASSWORD, PORT
import streamlit as st
def get_connection():
    conn=psycopg2.connect(
        host=st.secrets["HOST"],
        database=st.secrets["DATABASE"],
        user=st.secrets["USER"],
        password=st.secrets["PASSWORD"],
        sslmode="require"
    )
    return conn
