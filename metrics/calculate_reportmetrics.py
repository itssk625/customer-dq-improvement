import pandas as pd
from db.connection import get_connection
from collections import Counter
def calculate_report_metrics(id):
    conn=get_connection()
    cur=conn.cursor()
    cur.execute(f"""select count(*) from cleaned_customer_records where file_id=%s""",(id,))
    total=cur.fetchone()[0]
    cur.execute(f"""select count(*) from cleaned_customer_records where file_id=%s and is_validname and (is_validphoneno or is_validemail)""",(id,))
    total_valid=cur.fetchone()[0]
    total_invalid=total-total_valid
    cur.execute(f"""select count(*) from cleaned_customer_records where file_id=%s and not is_validdob""",(id,))
    invalid_dob_counts=cur.fetchone()[0]
    invalid_dob_pct=0 if (total==0) else (invalid_dob_counts/total)*100
    cur.execute(f"""select count(*) from cleaned_customer_records where file_id=%s and not is_validname""",(id,))
    invalid_name_counts=cur.fetchone()[0]
    invalid_name_pct=0 if (total==0) else (invalid_name_counts/total)*100
    cur.execute(f"""select count(*) from cleaned_customer_records where file_id=%s and not is_validphoneno""",(id,))
    invalid_phoneno_counts=cur.fetchone()[0]
    invalid_phoneno_pct=0 if (total==0) else (invalid_phoneno_counts/total)*100
    cur.execute(f"""select count(*) from cleaned_customer_records where file_id=%s and not is_validemail""",(id,))
    invalid_email_counts=cur.fetchone()[0]
    invalid_email_pct= 0 if (total==0) else (invalid_email_counts/total)*100
    query=f"""SELECT count(*) FROM cleaned_customer_records where file_id=%s and not is_validcountry"""
    cur.execute(query, (id,))
    invalid_country_counts = cur.fetchone()[0]
    invalid_country_pct=0 if (total==0) else  (invalid_country_counts/total)*100
    cur.execute(f"""select cleaned_email, cleaned_phoneno from cleaned_customer_records where file_id=%s""",(id,))
    rows=cur.fetchall()
    emails=[row[0] for row in rows if pd.notna(row[0])]
    phones=[row[1] for row in rows if pd.notna(row[1])]
    email_counts=Counter(emails)
    phoneno_counts=Counter(phones)
    email_duplc_counts=sum(count-1 for count in email_counts.values() if count>1)
    phoneno_duplc_counts=sum(count-1 for count in phoneno_counts.values() if count>1)
    print(email_duplc_counts, phoneno_duplc_counts)
    cur.execute(f"""insert into upload_metrics (file_id, total_records, total_valid_records, total_invalid_records, invalid_dob_pct, invalid_dob_counts, invalid_name_pct, invalid_name_counts, invalid_phoneno_pct, invalid_phoneno_counts, invalid_email_counts, invalid_email_pct, invalid_country_pct, invalid_country_counts,
                   duplicate_phone_counts, duplicate_email_counts) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s)""", (id,total, total_valid, total_invalid, invalid_dob_pct, invalid_dob_counts, invalid_name_pct, invalid_name_counts,invalid_phoneno_pct,invalid_phoneno_counts, invalid_email_counts,invalid_email_pct, invalid_country_pct, invalid_country_counts,
                   phoneno_duplc_counts, email_duplc_counts))
    conn.commit()
    cur.close()
    conn.close()
    
    
    