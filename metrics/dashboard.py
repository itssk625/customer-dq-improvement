import streamlit as st
import pandas as pd
from db.connection import get_connection
from visualization import display_metrics
def display_dashboard():
    st.title("Dashboard")
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
    '''col1, col2, col3=st.columns(3)
    with col1:
        st.metric(
            "Total Records", rec["total_records"]
        )
    with col2:
        st.metric(
            "Average DQ",
            round(rec["average_dq_score"],2)
        )
    with col3:
        if repo=="phone":
            st.metric(
                "Disposable Emails",
                f"{rec['disposable_email_pct']:.2f}%"
            )
    '''
    display_metrics(rec, showTitle=False)
        
    conn.close()