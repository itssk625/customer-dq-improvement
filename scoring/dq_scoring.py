import pandas as pd
import numpy as np
from db.connection import get_connection
import time
import streamlit as st

def score_dq():
    conn=get_connection()
    df=pd.read_sql_query("SELECT cleaned_email, name_issues, dob_issues, email_issues, phoneno_issues, nationality_issue, gender FROM final_CUSTOMER_email", conn)
    df=df.copy()
    cursor=conn.cursor()
    start=time.perf_counter()
    df['dq_score']=((df["email_issues"]).isna().astype(int)*25+(df['phoneno_issues']).isna().astype(int)*25
    +df["name_issues"].isna().astype(int)*15+df['dob_issues'].isna().astype(int)*10+df["nationality_issue"].isna().astype(int)*20
    +df['gender'].notna().astype(int)*5)
    st.write(time.perf_counter()-start)
    start=time.perf_counter()
    values=[(int(row["dq_score"]), row["cleaned_email"]) for _, row in df.iterrows()]
    st.write(time.perf_counter()-start)
    start=time.perf_counter()
    cursor.executemany("""update final_customer_email set dq_score=%s where cleaned_email=%s""", values)
    conn.commit()
    print(len(values))
    st.write(time.perf_counter()-start)
    
    
    df=pd.read_sql_query("SELECT cleaned_phoneno, name_issues, dob_issues, email_issues, phoneno_issues, nationality_issue, is_disposable_email, gender from final_customer_phone", conn)
    df=df.copy()
    start=time.perf_counter()
    df['email_score']=np.where(df["email_issues"].isna(), 25, 0)
    df['email_score']-=np.where((df["email_score"]==25) & df["is_disposable_email"].fillna(False), 10, 0)
    df['dq_score']=(df['email_score']+
        df['phoneno_issues'].isna().astype(int)*25
        +df["name_issues"].isna().astype(int)*15+df['dob_issues'].isna().astype(int)*10+df["nationality_issue"].isna().astype(int)*20
        +df['gender'].notna().astype(int)*5)
    st.write(time.perf_counter()-start)
    start=time.perf_counter()
    values=[(int(row["dq_score"]), row["cleaned_phoneno"]) for _, row in df.iterrows()]
    st.write(time.perf_counter()-start)

    start=time.perf_counter()
    cursor.executemany("""update final_customer_phone set dq_score=%s where cleaned_phoneno=%s""", values)
    print(len(values))
    st.write(time.perf_counter()-start)
    
    conn.commit()
    cursor.close()
    conn.close()
        
    