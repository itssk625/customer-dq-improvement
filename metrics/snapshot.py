import streamlit as st
import pandas as pd
from db.connection import get_connection
from metrics.visualization import display_dashboard_metrics
def display_snapshot_dashboard():
    conn=get_connection()
    months=pd.read_sql_query(
        """
        select distinct 
        date_trunc('month', snapshot_timestamp) as month
        from metrics
        order by month desc
        """, conn     
    )
    
    col1, col2=st.columns(2)
    with col1:
        repo=st.selectbox(
        "Repository",["email","phone"]
        )
    
    with col2:
        month=st.selectbox(
            "Month", months["month"], format_func=lambda x: x.strftime("%B %Y")
        )
    
    dashboard=pd.read_sql_query(
        """
        select * from metrics
        where repo_type=%s and date_trunc('month', snapshot_timestamp)=%s
        order by snapshot_timestamp desc
        limit 1
        """, conn, params=[repo, month]
    )
    
    if dashboard.empty:
        st.warning("No metrics available for selected month.")
        return 
    
    st.divider()
    rec=dashboard.iloc[0]
    display_dashboard_metrics(rec)
        
    conn.close()