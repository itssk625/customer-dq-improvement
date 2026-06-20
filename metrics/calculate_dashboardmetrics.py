import pandas as pd
from db.connection import get_connection

def calculate_dashboard_metrics():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(f"""select count(*) from master_customer_email""", conn)
    total=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from master_customer_email where not is_validdob""", conn)
    invalid_dob_counts=cursor.fetchone()[0]
    invalid_dob_pct=0 if (total==0) else  (invalid_dob_counts/total)*100
    cursor.execute(f"""select count(*) from master_customer_email where not is_validphoneno""", conn)
    invalid_phoneno_counts=cursor.fetchone()[0]
    invalid_phoneno_pct=0 if (total==0) else (invalid_phoneno_counts/total)*100
    query=f"""SELECT count(*) FROM master_customer_email where not is_validcountry;"""
    cursor.execute(query, conn)
    invalid_country_counts = cursor.fetchone()[0]
    invalid_country_pct=0 if (total==0) else  (invalid_country_counts/total)*100
    cursor.execute(f"""select avg(dq_score) from master_customer_email""", conn)
    dq_avg=cursor.fetchone()[0]
    cursor.execute(f"""insert into dashboard_metrics (total_records, invalid_dob_pct, invalid_dob_counts, invalid_phoneno_pct, invalid_phoneno_counts, invalid_country_pct, invalid_country_counts,
                   dq_score, repo_type) values (%s,%s,%s,%s, %s, %s, %s, %s, %s)""", (total, invalid_dob_pct, invalid_dob_counts, invalid_phoneno_pct, invalid_phoneno_counts, invalid_country_pct, invalid_country_counts,dq_avg, "email"))
    conn.commit()

    cursor.execute(f"""select count(*) from master_customer_phone""", conn)
    total=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from master_customer_phone where not is_validdob""", conn)
    invalid_dob_counts=cursor.fetchone()[0]
    invalid_dob_pct= 0 if (total==0) else (invalid_dob_counts/total)*100
    cursor.execute(f"""select count(*) from master_customer_phone where not is_validemail""", conn)
    invalid_email_counts=cursor.fetchone()[0]
    invalid_email_pct= 0 if (total==0) else (invalid_email_counts/total)*100
    query=f"""SELECT count(*) FROM master_customer_phone where not is_validcountry;"""
    cursor.execute(query, conn)
    invalid_country_counts = cursor.fetchone()[0]
    invalid_country_pct= 0 if (total==0) else (invalid_country_counts/total)*100
    cursor.execute(f"""select avg(dq_score) from master_customer_phone""", conn)
    dq_avg=cursor.fetchone()[0] or 0
    cursor.execute(f"""insert into dashboard_metrics (total_records, invalid_dob_pct, invalid_dob_counts, invalid_email_pct, invalid_email_counts, invalid_country_pct, invalid_country_counts,
                   dq_score, repo_type) values (%s,%s,%s,%s, %s, %s, %s, %s, %s)""", (total, invalid_dob_pct, invalid_dob_counts, invalid_email_pct, invalid_email_counts, invalid_country_pct, invalid_country_counts,dq_avg, "phoneno"))
    
    
    conn.commit()
    cursor.close()
    conn.close()