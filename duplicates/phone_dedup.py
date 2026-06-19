import pandas as pd
import numpy as np
from db.connection import get_connection
             
related_fields={
    "cleaned_name": ["is_validname","name_issues"],
    "cleaned_dob":["is_validdob", "dob_issues"],
    "cleaned_email":["is_validemail", "email_issues", "is_disposable_email", "email_classified_as", "extracted_domain"],
    "cleaned_phoneno": ["is_validphoneno", "phoneno_issues", "extracted_country", "extracted_operator"],
    "standardized_country":["is_validcountry", "nationality_issue"],
    "gender":[]
}

excluded_fields = {
    "file_id",
    "record_id",
    "is_emailduplicate",
    "is_phone_duplicate"
}

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
    duplc_phones=df['cleaned_phoneno'].duplicated(keep=False)
    df['is_phone_duplicate']=(duplc_phones & df['is_validphoneno'])
    
    phones=df['cleaned_phoneno'].dropna().unique()
    candidates=[]
    #consider all the fields reqd in the master table to create
    fields=['cleaned_name', 'cleaned_dob', 'cleaned_email', 'cleaned_phoneno', 'standardized_country',  'gender']
    for phone in phones:
        group=df[df['cleaned_phoneno']==phone]
        if (len(group)>1): 
            record={}
            for field in fields:
                for idx in group.index:
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
    conn=get_connection()
    query="""SELECT * FROM master_customer_phone WHERE cleaned_phoneno=%s"""
    fields=['cleaned_name', 'cleaned_dob', 'cleaned_email', 'cleaned_phoneno', 'standardized_country',  'gender']
    for phone in phones:
        group=df[df['cleaned_phoneno']==phone]
        golden_record=pd.read_sql_query(query, conn, params=[phone])
        record={}
        idx=group.index[0]
        if (golden_record.empty):
            record=(
                df.loc[idx]
                .drop(['file_id', 'is_emailduplicate', 'is_phone_duplicate', 'is_corrected'], errors="ignore")
            ).to_dict()
            if (pd.notna(record["cleaned_name"]) and pd.notna(record["cleaned_phoneno"])):
                insert_recs.append(record)
        else:
            master=golden_record.iloc[0].copy()
            if (pd.notna(master["cleaned_dob"])):
                master["cleaned_dob"]=pd.to_datetime(master["cleaned_dob"]).strftime("%d-%m-%Y")
            changed=False
            for field in fields:
                if field in excluded_fields:
                    continue
                else:
                    if pd.notna(df.loc[idx, field]):
                        record[field]=df.loc[idx, field]
                        for f in related_fields[field]:
                            record[f]=df.loc[idx, f]
                               
                    else:
                        record[field]=master[field]
                        for f in related_fields[field]:
                            record[f]=master[f]  
                     
                old_val=master[field]
                new_val=record[field]
                if (pd.isna(old_val) and pd.isna(new_val)):
                    continue
                elif (field=="cleaned_dob"):
                    if (pd.notna(record["cleaned_dob"])):
                        record["cleaned_dob"]=pd.to_datetime(record["cleaned_dob"]).strftime("%d-%m-%Y")
                    new_val=record[field]
                    if (old_val!=new_val):
                        changed=True
                elif (normalize(old_val)!=normalize(new_val)):
                    changed=True
            if (changed):
                update_recs.append(record)
    cursor=conn.cursor()
    for rec in insert_recs:
        cols=list(rec.keys())
        vals=[normalize(rec[col]) for col in cols]
        cols=",".join(cols)
        placeholders=",".join(["%s"]*len(rec))
        query=f"""
        INSERT INTO master_customer_phone ({cols}) values ({placeholders})
        """
        cursor.execute(query, tuple(vals))
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
        UPDATE master_customer_phone SET {set_clause} WHERE cleaned_phoneno=%s
        """
        
        vals=[normalize(rec[col]) for col in cols]
        vals.append(phone)
        cursor.execute(query, tuple(vals))
    conn.commit() 
    cursor.close()
    conn.close()

