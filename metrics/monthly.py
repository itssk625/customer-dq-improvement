import streamlit as st
import pandas as pd
from db.connection import get_connection

import plotly.graph_objects as go

def display_chart(df, title_, y_col, y_label, suffix=""):
    fig=go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["month"],
            y=df[y_col],
            mode="markers"
        )
    )
    fig.update_layout(
        title=title_,
        xaxis_title="Month",
        yaxis_title=y_label,
        template="plotly_dark", height=450, plot_bgcolor="#0e1117", paper_bgcolor="#0e1117")
    
    fig.update_xaxes(
        showgrid=False, zeroline=False
    )
    
    fig.update_yaxes(
        ticksuffix=suffix,
        showgrid=False, zeroline=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
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
    
    display_chart(dq_trend, title_="Month-on-Month DQ Score", y_col='average_dq_score',y_label="DQ Score", suffix="%")
    
    repo_trend=pd.read_sql_query("""select distinct on (date_trunc('month', snapshot_timestamp))
                                 date_trunc('month', snapshot_timestamp) as month,
                                 total_records from metrics where repo_type=%s order by date_trunc('month', snapshot_timestamp),
                                 snapshot_timestamp desc""", conn, params=[repo])
    
    repo_trend['month']=repo_trend['month'].dt.strftime("%b %Y")
    
    display_chart(repo_trend, title_="Month-on-Month Record Growth", y_col='total_records', y_label='Total Records')
    
    st.write("Attribute-wise Validity Improvement")
    attributes=['valid_name_count', 'valid_dob_count', 'valid_email_count', 'valid_phoneno_count', 'valid_gender_count', 'valid_country_count']
    
    name_trend=pd.read_sql_query("""select distinct on (date_trunc('month', snapshot_timestamp))
                            date_trunc('month', snapshot_timestamp) as month,
                            round((valid_name_count::numeric/total_records)*100,2) as valid_name_pct from metrics where repo_type=%s 
                            order by date_trunc('month', snapshot_timestamp), snapshot_timestamp desc""", conn, params=[repo])
    
    name_trend['month']=name_trend['month'].dt.strftime("%b %Y")
    
    display_chart(name_trend, title_="Month-on-Month Name Validity Improvement", y_col='valid_name_pct', y_label='Name Validity (%)', suffix="%")
    