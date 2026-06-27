import streamlit as st
import plotly.graph_objects as go
from visualization import display_report_metrics
    
def display_report(report_df):
    st.subheader("Customer Data Quality Report", text_alignment="center")
    email_repo=report_df.query("repo_type=='email'")
    phone_repo=report_df.query("repo_type=='phone'")
    if not email_repo.empty:
            display_report_metrics(email_repo.iloc[0])
    if not phone_repo.empty:
            st.divider()
            display_report_metrics(phone_repo.iloc[0])
    st.divider()
