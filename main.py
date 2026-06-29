import pandas as pd
import numpy as np
from validation.dob_validation import validate_dobs
from validation.name_validation import validate_names
from validation.email_validation import validate_emails
from validation.phone_validation import validate_phones
from standardization.dob_standardization import standardize_dobs
from standardization.name_standardization import standardize_names
from standardization.email_standardization import standardize_emails
from standardization.country_standardization import standardize_country
from standardization.gender_standardization import standardize_gender
from enrichment.email_enrichment import enrich_emails
from enrichment.phone_enrichment import enrich_phones
from duplicates.email_dedup import dedup_emails
from duplicates.phone_dedup import dedup_phones
from enrichment.risk_scoring import score_risk
from scoring.dq_scoring import score_dq
from metrics.calculate_metrics import calculate_metrics
from db.connection import get_connection
from metrics.report import display_report
from metrics.dashboard import display_dashboard
from io import StringIO
import streamlit as st
import uuid

st.set_page_config(layout="wide")

def validate_file(df):
    required_columns=['first_name', 'last_name', 'dob', 'country', 'gender', 'email', 'phone_no']
    if df.empty:
        raise ValueError("Uploaded file is empty.")
    missing=set(required_columns)-set(df.columns)
    if missing: 
        raise ValueError(f"Missing columns: {missing}")
    extra=set(df.columns)-set(required_columns)
    if extra:
        print(f"Warning: Extra columns {extra} will be ignored")
        df=df[required_columns]
    return df
    
def main():
    if "processed" not in st.session_state:
        st.session_state.processed=False
    if "report" not in st.session_state:
        st.session_state.report=None
    if "downloads" not in st.session_state:
        st.session_state.downloads={}
    if "email_valid" not in st.session_state:
        st.session_state.email_valid=False
    if "phone_valid" not in st.session_state:
        st.session_state.phone_valid=False
    st.title("Customer DQ Improvement")
    page=st.segmented_control(
        "", ["Upload","Dashboard"],
        default="Upload"
    )
    conn=get_connection()
    cursor=conn.cursor()        
    try:
        if page=="Upload":
            uploaded_file=st.file_uploader("Upload CSV", type=["csv"])
            if uploaded_file and st.button("Process file"):
                file_id=str(uuid.uuid4())
                df=pd.read_csv(uploaded_file)
                df=validate_file(df)
                if df['email'].isna().all() and df['phone_no'].isna().all():
                        raise ValueError("Email and phone columns are empty: No valid data available for processing")
                with st.spinner("Processing records..."):
                    
                    df["file_id"]=file_id
                    df=df[["file_id",
                            "first_name",
                            "last_name",
                            "dob",
                            "country",
                            "gender",
                            "email",
                            "phone_no"]]
                    buffer = StringIO()
                    df.to_csv(buffer, index=False)
                    buffer.seek(0)

                    cursor.copy_expert(
                        """
                        COPY raw_customer_records
                        (
                            file_id,
                            first_name,
                            last_name,
                            dob,
                            country,
                            gender,
                            email,
                            phone_no
                        )
                        FROM STDIN
                        WITH CSV HEADER
                        """,
                        buffer
                    )
                    conn.commit()
                    df['extracted_country']=np.nan
                    df['extracted_operator']=np.nan
                    
                    #validation
                    df=validate_names(df)

                    df=validate_dobs(df)

                    df=validate_phones(df)
                    df=validate_emails(df)
                    #standardization
                    df=standardize_names(df)
                    df=standardize_dobs(df)
                    df=standardize_emails(df)
                    df=standardize_country(df)
                    df=standardize_gender(df)
                    df=enrich_emails(df)
                    df=enrich_phones(df)
                    df=score_risk(df)

                    df=df[['file_id','cleaned_name','cleaned_dob', 'cleaned_email','cleaned_phoneno', 'standardized_country','name_issues','dob_issues', 'email_issues','phoneno_issues','email_classified_as','extracted_domain', 'extracted_operator','extracted_country','risk_score','cleaned_gender','iso_code','nationality_issue', 'gender_issues','is_disposable_email']]
                    df['risk_score']=df["risk_score"].astype("Int64")
                    buffer=StringIO()
                    df.to_csv(buffer, index=False, header=False)
                    buffer.seek(0)
                    cursor.copy_expert(
                        """
                        COPY cleaned_customer_records(file_id,
                            cleaned_name,
                            cleaned_dob,cleaned_email,cleaned_phoneno,standardized_country,
                            name_issues,dob_issues,email_issues,phoneno_issues,
                            email_classified_as,extracted_domain, extracted_operator, extracted_country,
                            risk_score,gender,iso_code,nationality_issue, gender_issues, is_disposable_email
                        )
                        FROM STDIN
                        WITH CSV
                        """, buffer
                        
                    )
                    conn.commit()
                    print('.')
                    df=pd.read_sql_query("select file_id,record_id,cleaned_name,cleaned_dob, cleaned_email,cleaned_phoneno, standardized_country,name_issues,dob_issues, email_issues,phoneno_issues, is_disposable_email,email_classified_as,extracted_domain, extracted_operator,extracted_country,risk_score,gender,iso_code,nationality_issue, gender_issues from cleaned_customer_records where file_id=%s", conn, params=[file_id])
                    dedup_emails(df)
                    dedup_phones(df)
                    
                    score_dq()
                    calculate_metrics()
                    report=pd.read_sql_query(
                    """select distinct on (repo_type) * from metrics order by repo_type, snapshot_timestamp desc""", conn
                    )
                    
                    golden_phone=pd.read_sql_query("""select * from final_customer_phone order by record_id""", conn)
                    golden_email=pd.read_sql_query("""select * from final_customer_email order by record_id""", conn)
                    if (golden_email.empty and golden_phone.empty):
                        st.warning("No valid records were found. Tables were not populated")      
                        st.session_state.email_valid=False
                        st.session_state.phone_valid=False
                    elif (golden_phone.empty):
                        st.warning("No valid phone-identified records were found")                    
                        st.session_state.email_valid=True
                        st.session_state.phone_valid=False
                    elif (golden_email.empty):
                        st.warning("No valid email-identified records were found")
                        st.session_state.email_valid=False
                        st.session_state.phone_valid=True
                    else:
                        st.session_state.email_valid=True
                        st.session_state.phone_valid=True
                    st.session_state.report=report
                    st.session_state.downloads={
                        "golden_email":golden_email,
                        "golden_phone":golden_phone,
                        "golden_rec_email":golden_email.to_csv(index=False),
                        "golden_rec_phone":golden_phone.to_csv(index=False),                      
                    }
                    st.session_state.processed=True
                    if (st.session_state.email_valid or st.session_state.phone_valid):
                        st.success("Processing completed successfully!")
                    cursor.close()
                    conn.close()
            if st.session_state.processed:
                st.divider()
                if (st.session_state.email_valid):
                    st.subheader("Email identified records")
                    st.dataframe(st.session_state.downloads["golden_email"].head(10))
                if (st.session_state.phone_valid):
                    st.subheader("Phone identified records")
                    st.dataframe(st.session_state.downloads["golden_phone"].head(10))
                
                if (st.session_state.email_valid or st.session_state.phone_valid):
                    #display_report(st.session_state.report)
                    st.iframe("http://localhost:3000/public/dashboard/3f2aa9b2-fafc-4966-9f57-49772dd29132", height=1500)
                                    
                if (st.session_state.email_valid or st.session_state.phone_valid):
                    st.subheader("Downloads")
                if (st.session_state.email_valid):
                    st.download_button("Download final email table", st.session_state.downloads["golden_rec_email"], file_name="golden_recs_email.csv",
                        mime="text/csv")
                if (st.session_state.phone_valid):
                    st.download_button("Download final phone table", st.session_state.downloads["golden_rec_phone"], file_name="golden_recs_phone.csv",
                        mime="text/csv")
        
        elif page=="Dashboard":
            st.iframe("http://localhost:3000/public/dashboard/11228b8c-2254-4f87-b1c6-31592323ee11#night", height=2000)

    except Exception as e:
        st.error(f"Error: {e}")
        raise
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
    
if __name__=='__main__':
    main()
    
