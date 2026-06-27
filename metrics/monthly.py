import streamlit as st
import pandas as pd
from db.connection import get_connection

import plotly.graph_objects as go

def get_trend(conn, repo, column):
    query=f"""
    select distinct on (date_trunc('month', snapshot_timestamp))
                            date_trunc('month', snapshot_timestamp) as month,
                            round(({column}::numeric/total_records)*100,2) as validity_pct from metrics where repo_type=%s 
                            order by date_trunc('month', snapshot_timestamp), snapshot_timestamp desc
    
    """
    df=pd.read_sql_query(query, conn, params=[repo])
    df['month']=df['month'].dt.strftime("%b %Y")
    return df

def display_chart(df, title_, y_col, y_label, suffix="", y_range=None):
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
        showgrid=False, zeroline=False, range=y_range
    )
    if y_range is not None:
        fig.update_yaxes(range=y_range)
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
    
    display_chart(dq_trend, title_="Month-on-Month DQ Score", y_col='average_dq_score',y_label="DQ Score", suffix="%", y_range=[0,100])
    
    repo_trend=pd.read_sql_query("""select distinct on (date_trunc('month', snapshot_timestamp))
                                 date_trunc('month', snapshot_timestamp) as month,
                                 total_records from metrics where repo_type=%s order by date_trunc('month', snapshot_timestamp),
                                 snapshot_timestamp desc""", conn, params=[repo])
    
    repo_trend['month']=repo_trend['month'].dt.strftime("%b %Y")
    
    display_chart(repo_trend, title_="Month-on-Month Record Growth", y_col='total_records', y_label='Total Records')
    
    st.subheader("Attribute-wise Validity Improvement")
    charts=[('valid_name_count',"Name"),( 'valid_dob_count', "DOB"), ('valid_gender_count',"Gender"),('valid_country_count', "Country")]
    
    if repo=="email":
        phoneno_trend=get_trend(conn, repo, "valid_phoneno_count")
        display_chart(phoneno_trend, title_="Month-on-Month Phone Number Validity Improvement", y_col='validity_pct', y_label='Phone Number Validity (%)', suffix="%", y_range=[0,100])
    elif repo=="phone":
        email_trend=get_trend(conn, repo, "valid_email_count")
        display_chart(email_trend, title_="Month-on-Month Email Validity Improvement", y_col='validity_pct', y_label='Email Validity (%)', suffix="%", y_range=[0,100])
    for column, title in charts:
        trend=get_trend(conn, repo, column)
        display_chart(trend, title_=f"Month-on-Month {title} Validity Improvement", y_col='validity_pct', y_label=f"{title} Validity (%)", suffix="%", y_range=[0,100])
    
    