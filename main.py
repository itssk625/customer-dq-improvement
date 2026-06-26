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
from metrics.calculate_dashboardmetrics import calculate_dashboard_metrics
from db.connection import get_connection
from metrics.report import display_report
from io import StringIO
import streamlit as st
import uuid


def main():
    st.title("Customer DQ Improvement")
    if "processed" not in st.session_state:
        st.session_state.processed=False
    if "report" not in st.session_state:
        st.session_state.report=None
    if "downloads" not in st.session_state:
        st.session_state.downloads={}
    try:
        uploaded_file=st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file and st.button("Process file"):
            file_id=str(uuid.uuid4())
            df=pd.read_csv(uploaded_file)
            with st.spinner("Processing records..."):
                conn=get_connection()
                cursor=conn.cursor()
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
                #df=enrich_phones(df)
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
                calculate_dashboard_metrics()
                report=pd.read_sql_query(
                """select distinct on (repo_type) * from metrics order by repo_type, snapshot_timestamp desc""", conn
                )
                
                golden_phone=pd.read_sql_query("""select * from final_customer_phone""", conn)
                golden_email=pd.read_sql_query("""select * from final_customer_email""", conn)
                st.session_state.report=report
                st.session_state.downloads={
                    "golden_rec_email":golden_email.to_csv(index=False),
                    "golden_rec_phone":golden_phone.to_csv(index=False),                      
                }
                st.session_state.processed=True
                st.success("Processing completed successfully!")
                cursor.close()
                conn.close()
        if st.session_state.processed:
            st.divider()
            display_report(st.session_state.report)
            st.subheader("Downloads")
            st.download_button("Download final email table", st.session_state.downloads["golden_rec_email"], file_name="golden_recs_email.csv",
                mime="text/csv")
            st.download_button("Download final phone table", st.session_state.downloads["golden_rec_phone"], file_name="golden_recs_phone.csv",
                mime="text/csv")

    except Exception as e:
        st.error(f"Error: {e}")
        raise
    
    
if __name__=='__main__':
    main()
    
