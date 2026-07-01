import pandas as pd
import numpy as np
from db.connection import get_connection
from psycopg2.extras import execute_values            
related_fields={
    "cleaned_name": ["name_issues"],
    "cleaned_dob":["dob_issues"],
    "cleaned_email":["email_issues", "is_disposable_email","email_classified_as", "extracted_domain"],
    "cleaned_phoneno": [ "phoneno_issues", "extracted_country", "extracted_operator"],
    "standardized_country":["nationality_issue", "iso_code"],
    "gender":['gender_issues']
}

def calculate_dq(record):
    score=0
    if pd.isna(record['email_issues']):
        score += 25

    if pd.isna(record["phoneno_issues"]):
        score += 25

    if pd.isna(record["name_issues"]):
        score += 15

    if pd.isna(record["dob_issues"]):
        score += 10

    if pd.isna(record["nationality_issue"]):
        score += 20

    if pd.notna(record["gender"]):
        score += 5

    if (
        pd.isna(record["email_issues"])
        and record.get("is_disposable_email", False)
    ):
        score -= 10
    return score

def normalize(v):
    if pd.isna(v):
        return None
    if isinstance(v, np.bool_):
        return bool(v)
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        return float(v)
    return v

def dedup_phones(df):
    df=df.copy()
    df=df.sort_values("record_id")
    candidates=[]
    fields=['cleaned_name', 'cleaned_dob', 'cleaned_email', 'cleaned_phoneno', 'standardized_country',  'gender', 'upload_date']
    for phone,group in df.groupby("cleaned_phoneno"):
        group=group.sort_values('record_id')
        if (len(group)>1): 
            record={}
            for field in fields:
                for idx in group.index:
                    if field=='upload_date':
                        if field not in record:
                            record[field]=df.loc[idx, field]
                        elif field in record:
                            record[field]=max(record[field], df.loc[idx, field])
                        continue
                    if field not in record or pd.notna(df.loc[idx, field]):
                        record[field] = df.loc[idx, field]
                        for f in related_fields[field]:
                            record[f] = df.loc[idx, f]
            candidates.append(record)
                        
        else:
            idx=group.index[0]
            record=df.loc[idx].to_dict()
            candidates.append(record)
    
    master_candidates=pd.DataFrame(candidates)    
    merge_phones_master(master_candidates)

def merge_phones_master(df):
    df=df.copy()
    insert_recs=[]
    update_recs=[]
    phones=df['cleaned_phoneno'].dropna().unique()
    if len(phones)==0:
        return
    conn=get_connection()
    cursor=conn.cursor()
    placeholders=",".join(["%s"]*len(phones))
    query=f"""SELECT * FROM final_customer_phone WHERE cleaned_phoneno in ({placeholders})"""
    golden_records=pd.read_sql_query(query, conn, params=phones)
    golden_records=golden_records.set_index("cleaned_phoneno")
    fields=['cleaned_name', 'cleaned_dob', 'cleaned_email', 'cleaned_phoneno', 'standardized_country',  'gender', 'upload_date']
    for phone, group in df.groupby("cleaned_phoneno"):
        record={}
        idx=group.index[0]
        if phone in golden_records.index:
            master=golden_records.loc[phone].copy()
        
            changed=False
            for field in fields:
                if field=='upload_date':
                    record[field]=max(master[field],df.loc[idx, field])
                    continue
                if pd.notna(df.loc[idx, field]):
                    record[field]=df.loc[idx, field]
                    for f in related_fields[field]:
                        record[f]=df.loc[idx, f]
                               
                else:
                    record[field]=master[field]
                    for f in related_fields[field]:
                        record[f]=master[f]  
                if (field=="cleaned_phoneno"):
                    old_val=phone
                else:
                    old_val=master[field]
                new_val=record[field]
                if (pd.isna(old_val) and pd.isna(new_val)):
                    continue
              
                if (old_val!=new_val):
                    changed=True
                elif (normalize(old_val)!=normalize(new_val)):
                    changed=True
            if (changed):
                record['dq_score']=calculate_dq(record)
                update_recs.append(record)
        else:
            record=(
                df.loc[idx]
                .drop(['record_id','file_id', 'risk_score','is_emailduplicate', 'is_phone_duplicate', 'is_corrected'], errors="ignore")
            ).to_dict()
         
            if (pd.notna(record["cleaned_phoneno"])):
                record["dq_score"]=calculate_dq(record)
                insert_recs.append(record)
    if insert_recs:
        cols=list(insert_recs[0].keys())
        vals=[tuple(normalize(rec[col]) for col in cols)  for rec in insert_recs]
        cols=",".join(cols)
        query=f"""
        INSERT INTO final_customer_phone ({cols}) values %s
        """
        execute_values(cursor, query, vals)
        conn.commit()
    for rec in update_recs:
        phone=rec["cleaned_phoneno"]
        cols=[
            col 
            for col in rec.keys()
            if col!= "cleaned_phoneno" 
        ]
        set_clause=",".join(
            [f"{col}=%s" for col in cols]
        )
        set_clause+= ", last_updated_timestamp=CURRENT_TIMESTAMP"
        query=f"""
        UPDATE final_customer_phone SET {set_clause} WHERE cleaned_phoneno=%s
        """
        
        vals=[normalize(rec[col]) for col in cols]
        vals.append(phone)
        cursor.execute(query, tuple(vals))
    conn.commit() 
    cursor.close()
    conn.close()

