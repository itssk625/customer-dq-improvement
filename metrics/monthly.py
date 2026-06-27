import streamlit as st
import pandas as pd
from db.connection import get_connection

import plotly.graph_objects as go

def display_monthly_dashboard():
    conn=get_connection()
    c1, c2=st.columns(2)
    with c1:
        repo=st.selectbox(
            "Repository",["email","phone"]
        )
    
    dq_trend=pd.read_sql_query("""select distinct on (date_trunc('month',snapshot_timestamp))
                               date_trunc('month', snapshot_timestamp) as month,
                               average_dq_score
                               from metrics where repo_type=%s
                               order by date_trunc('month', snapshot_timestamp), snapshot_timestamp desc""", conn, params=[repo])
    dq_trend['month']=dq_trend['month'].dt.strftime("%b %Y")
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dq_trend["month"],
            y=dq_trend["average_dq_score"],
            mode="markers",
            name="Average DQ Score"
        )
    )
    fig.update_layout(
        title="Month-on-Month Average DQ Score",
        xaxis_title="Month",
        yaxis_title="Average DQ Score",
        template="plotly_dark", height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    repo_trend=pd.read_sql_query("""select distinct on (date_trunc('month', snapshot_timestamp))
                                 date_trunc('month', snapshot_timestamp) as month,
                                 total_records from metrics where repo_type=%s order by date_trunc('month', snapshot_timestamp),
                                 snapshot_timestamp desc""")
    
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(
            x=repo_trend['month'],
            y=repo_trend['total_records'],
            mode="markers",
            name="Record Growth"
        )
    )
    fig.update_layout(
        title="Month-on-Month Record Growth",
        xaxis_title="Month",
        yaxis_title="Total Records",
        template="plotly_dark", height=450
    )
    st.plotly_chart(fig, use_container_width=True)