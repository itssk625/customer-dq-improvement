import pandas as pd
from db.connection import get_connection
from calendar import monthrange

def calculate_metrics():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(f"""select count(*) from final_customer_email""")
    total=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where cleaned_name is not null""")
    valid_name_counts=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where cleaned_dob is not null""")
    valid_dob_counts=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where cleaned_phoneno is not null""" )
    valid_phoneno_counts=cursor.fetchone()[0]
    query=f"""SELECT count(*) FROM final_customer_email where  standardized_country is not null"""
    cursor.execute(query)
    valid_country_counts = cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where gender is not null""")
    valid_gender_counts=cursor.fetchone()[0]
    cursor.execute(f"""select avg(dq_score) from final_customer_email""")
    dq_avg=cursor.fetchone()[0]
    cursor.execute(f"""select upload_date from final_customer_email""")
    mdate=cursor.fetchone()[0]
    year=mdate.year
    month=mdate.month
    last_day=monthrange(year, month)[1]
    snapshot_timestamp=mdate.replace(day=last_day)
    cursor.execute(f"""insert into metrics (snapshot_timestamp, repo_type,total_records, valid_name_count, valid_dob_count, valid_phoneno_count, valid_country_count, valid_gender_count,
                   average_dq_score) values (%s,%s,%s,%s,%s, %s, %s, %s, %s)""", (snapshot_timestamp,"email",total, valid_name_counts, valid_dob_counts,valid_phoneno_counts, valid_country_counts, valid_gender_counts,dq_avg))
    conn.commit()
    
    cursor.execute(f"""select count(*) from final_customer_phone""")
    total=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_phone where cleaned_name is not null""")
    valid_name_counts=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_phone where cleaned_dob is not null""")
    valid_dob_counts=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_phone where cleaned_email is not null""")
    valid_email_counts=cursor.fetchone()[0]
    query=f"""SELECT count(*) FROM final_customer_phone where standardized_country is not null"""
    cursor.execute(query)
    valid_country_counts = cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_phone where gender is not null""")
    valid_gender_counts=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_phone where is_disposable_email""")
    disposable_counts=cursor.fetchone()[0]
    disposable_pct=0 if (disposable_counts==0) else (disposable_counts/total)*100
    cursor.execute(f"""select avg(dq_score) from final_customer_phone""")
    dq_avg=cursor.fetchone()[0]
    cursor.execute(f"""select upload_date from final_customer_email""")
    mdate=cursor.fetchone()[0]
    year=mdate.year
    month=mdate.month
    last_day=monthrange(year, month)[1]
    snapshot_timestamp=mdate.replace(day=last_day)
    cursor.execute(f"""insert into metrics (snapshot_timestamp,repo_type,total_records, valid_name_count, valid_dob_count, valid_email_count, valid_country_count, valid_gender_count, disposable_email_pct,
                   average_dq_score) values (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)""", (snapshot_timestamp"phone",total, valid_name_counts, valid_dob_counts,valid_email_counts, valid_country_counts, valid_gender_counts,disposable_pct,dq_avg))
    conn.commit()
    cursor.close()
    conn.close()
    