import streamlit as st
import pandas as pd
from metrics.snapshot import display_snapshot_dashboard
from metrics.monthly import display_monthly_dashboard

def display_dashboard():
    view=st.radio("Dashboard View", ["DQ Snapshot", "Month-on-Month"], horizontal=True)
    st.title("Data Monitoring Dashboard")
    if view=="DQ Snapshot":
        display_snapshot_dashboard()
    elif view=="Month-on-Month":
        display_monthly_dashboard()
    