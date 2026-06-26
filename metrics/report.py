import streamlit as st
import plotly.graph_objects as go

def circ_progress(title, valid_count, total):
    pct=0 if valid_count==0 else round((valid_count/total)*100,2)
    fig=go.Figure(
        go.Pie(
            values=[pct, 100-pct],
            hole=.88,
            marker=dict(
                colors=["#22c55e", "#d1d5db"]
            ),
            textinfo="none",
            showlegend=False
        )
    )
    fig.update_layout(
        annotations=[
            dict(
                text=f"<b>{pct}%</b>",
                x=.5, y=.5,
                showarrow=False, font=dict(size=15, family="Arial Black")
            )
        ],
        title={
            "text": f"<b>{title}</b>",
            "x": .5,
            "font":{
                "size":15
            }
        },
        margin=dict(l=5, r=5, t=40, b=5),
        height=240,
        width=240
    )
    
    st.plotly_chart(fig)
    st.markdown(
        f"""
        <div style="
        text-align;center;
        font-size=17px;
        color: #bfbfbf;
        margin-top: -8px;
        ">
        {valid_count}/{total} Valid
        </div>
        """,
        unsafe_allow_html=True
    )
    
def display_metrics(rec):
    
    total=rec["total_records"]
    if (rec["repo_type"]=="email"):
        st.subheader("Metrics for email identified records")
    else:
        st.subheader("Metrics for phone identified records")
    
    col1, col2, col3=st.columns(3)
    with col1:
        circ_progress("Name", rec["valid_name_count"],total)
    with col2:
        circ_progress("DOB", rec["valid_dob_count"], total)
    with col3:
        if rec["repo_type"]=="email":
            circ_progress("Phone number", rec["valid_phoneno_count"], total)
        else:
            circ_progress("Email", rec["valid_email_count"], total)
    
    col1, col2=st.columns(2)
    with col1:
        circ_progress("Country", rec["valid_country_count"], total)
    with col2:
        circ_progress("Gender", rec["valid_gender_count"], total)
        
    st.divider()
    
    col1, col2, col3=st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div style="text-align:center;"
            padding-top:5px;
            >
                <div style="
                    font-size: 15px;
                    color:#bfbfbf;
                    font-weight:500;
                    font-family:Arial, sans-serif;
                ">
                    Total Records
                </div>
                </div style="
                    font-size:20px;
                    font-weight:700;
                    font-family: Arial, sans-serif;
                    line-height:1,2;
                ">
                    {rec["total_records"]}
                </div>
            </div>
        """,
        unsafe_allow_html=True,
        )
        
    with col2:
        st.metric(st.markdown(
            f"""
            <div style="text-align:center;"
            padding-top:5px;
            >
                <div style="
                    font-size: 15px;
                    color:#bfbfbf;
                    font-weight:500;
                    font-family:Arial, sans-serif;
                ">
                    Average DQ score 
                </div>
                </div style="
                    font-size:20px;
                    font-weight:700;
                    font-family: Arial, sans-serif;
                    line-height:1,2;
                ">
                    {round(rec["average_dq_score"],2)}
                </div>
            </div>
        """,
        unsafe_allow_html=True,
        )
        )
    
    with col3:
        if (rec["repo_type"]=="phone"):
            st.markdown(
            f"""
            <div style="text-align:center;"
            padding-top:5px;
            >
                <div style="
                    font-size: 15px;
                    color:#bfbfbf;
                    font-weight:500;
                    font-family:Arial, sans-serif;
                ">
                    Disposable Emails
                </div>
                </div style="
                    font-size:20px;
                    font-weight:700;
                    font-family: Arial, sans-serif;
                    line-height:1,2;
                ">
                    {rec['disposable_email_pct']}
                </div>
            </div>
        """,
        unsafe_allow_html=True,
        )
        
    
def display_report(report_df):
    st.subheader("DQ Report")
    email_repo=report_df.query("repo_type=='email'").iloc[0]
    phone_repo=report_df.query("repo_type=='phone'").iloc[0]
    if not email_repo.empty:
            display_metrics(email_repo)
    if not phone_repo.empty:
            display_metrics(phone_repo)
    st.divider()
