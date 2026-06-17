import pandas as pd

from db.connection import get_connection
related_fields={
    "concatenated_name": ["is_validname","name_issue"],
    "valid_dob":["is_validdob", "dob_issue"],
    "valid_emails":["is_validemail", "email_issue", "is_disposable", "email_type", "suggested_domain"],
    "valid_phone": ["is_validphoneno", "phoneno_issues", "extracted_country", "extracted_operator"],
    "valid_nationality":["is_validnationality", "nationality_issue"],
    "gender":[]
                
}
def dedup_emails_upload(df):
    df=df.copy()
    duplc_emails=df['valid_emails'].duplicated(keep=False)
    df['is_emailduplicate']=(duplc_emails & df['is_validemail'])
    print(df[['valid_emails','is_validemail','is_emailduplicate']])
    emails=df['valid_emails'].dropna().unique()
    candidates=[]
    #consider all the fields reqd in the master table to create
    fields=['concatenated_name', 'valid_dob', 'valid_emails', 'valid_phone', 'valid_nationality',  'gender']
    for email in emails:
        group=df[df['valid_emails']==email]
        if (len(group)>1): 
            record={}
            for field in fields:
                for idx in group.index:
                    if field not in record and pd.notna(df.loc[idx, field]):
                        record[field]=df.loc[idx, field]
                        for f in related_fields[field]:
                            record[f]=df.loc[idx, f]
            candidates.append(record)
                        
        else:
            idx=group.index[0]
            record=df.loc[idx].to_dict()
            candidates.append(record)
    
    master_candidates=pd.DataFrame(candidates)    
    merge_emails_master(master_candidates)

def merge_emails_master(df):
    df=df.copy()
    insert_recs=[]
    update_recs=[]
    emails=df['valid_emails'].dropna().unique()
    conn=get_connection()
    query="""SELECT * FROM master_customer_email WHERE cleaned_email=%s"""
    fields=['concatenated_name', 'valid_dob', 'valid_emails', 'valid_phone', 'valid_nationality',  'gender']
    for email in emails:
        group=df[df['valid_emails']==email]
        golden_record=pd.read_sql_query(query, conn, params=[email])
        record={}
        idx=group.index
        if (golden_record.empty):
            insert_recs.extend(df.loc[idx].to_dict(orient='records'))
        else:
            for field in fields:
                for idx in group.index:
                    if pd.notna(df.loc[idx, field]):
                        record[field]=df.loc[idx, field]
                        for f in related_fields[field]:
                            record[f]=df.loc[idx, f]
                    else:
                        record[field]=golden_record[]
            update_recs.append(record)
                        
    
    
    
    
    return df

