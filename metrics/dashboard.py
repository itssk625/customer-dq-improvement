import streamlit as st
import pandas as pd
from db.connection import get_connection
def display_dashboard():
    st.title("Dashboard")
    conn=get_connection()
    dashboard=pd.read_sql_query(
        """select * from metrics order by snapshot_timestamp desc""", conn
    )
    st.dataframe(dashboard)
    conn.close()