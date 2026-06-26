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
    months=pd.read_sql_query(
        """
        select distinct 
        date_trunc('month', snapshot_timestamp) as month
        from metrics
        order by month desc
        """, conn     
    )
    repo=st.selectbox(
        "Repository",["email","phone"]
    )
    month=st.selectbox(
        "Month", months["month"]
    )
    
    dashboard=pd.read_sql_query(
        """
        select * from metrics
        where repo_type=%s and date_trunc('month', snapshot_timestamp)=DATE_TRUNC('month',%s::timestamp)
        order by snapshot_timestamp desc
        limit 1
        """, conn, params=[repo, month]
    )
    rec=dashboard.iloc[0]
    col1, col2, col3=st.columns(3)
    with col1:
        st.metric(
            "Total Records", rec["total_records"]
        )
    with col2:
        st.metric(
            "Average DQ",
            round(rec["avergae_dq_score"],2)
        )
    with col3:
        if repo=="phone":
            st.metric(
                "Disposable Emails",
                f"{rec["disposable_email_pct"]:.2f}%"
            )
    conn.close()