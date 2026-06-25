import pandas as pd
from db.connection import get_connection

def calculate_dashboard_metrics():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(f"""select count(*) from final_customer_email""", conn)
    total=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where cleaned_name is not null""", conn)
    valid_name_counts=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where cleaned_dob is not null""", conn)
    valid_dob_counts=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where cleaned_phoneno is not null""", conn)
    valid_phoneno_counts=cursor.fetchone()[0]
    query=f"""SELECT count(*) FROM final_customer_email where  standardized_country is not null;"""
    cursor.execute(query, conn)
    valid_country_counts = cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_email where gender is not null""", conn)
    valid_gender_counts=cursor.fetchone()[0]
    cursor.execute(f"""select avg(dq_score) from final_customer_email""", conn)
    dq_avg=cursor.fetchone()[0]
    cursor.execute(f"""insert into metrics (repo_type,total_records, valid_name_count, valid_dob_count, valid_phoneno_count, valid_country_count, valid_gender_count,
                   average_dq_score) values (%s,%s,%s,%s, %s, %s, %s, %s)""", ("email",total, valid_name_counts, valid_dob_counts,valid_phoneno_counts, valid_country_counts, valid_gender_counts,dq_avg))
    conn.commit()
    cursor.close()
    conn.close()
'''
    cursor.execute(f"""select count(*) from final_customer_phone""", conn)
    total=cursor.fetchone()[0]
    cursor.execute(f"""select count(*) from final_customer_phone where cleaned_dob is null""", conn)
    invalid_dob_counts=cursor.fetchone()[0]
    invalid_dob_pct= 0 if (total==0) else (invalid_dob_counts/total)*100
    cursor.execute(f"""select count(*) from final_customer_phone where cleaned_email is null""", conn)
    invalid_email_counts=cursor.fetchone()[0]
    invalid_email_pct= 0 if (total==0) else (invalid_email_counts/total)*100
    query=f"""SELECT count(*) FROM final_customer_phone where standardized_country is null;"""
    cursor.execute(query, conn)
    invalid_country_counts = cursor.fetchone()[0]
    invalid_country_pct= 0 if (total==0) else (invalid_country_counts/total)*100
    cursor.execute(f"""select avg(dq_score) from final_customer_phone""", conn)
    dq_avg=cursor.fetchone()[0] or 0
    cursor.execute(f"""insert into dashboard_metrics (total_records, invalid_dob_pct, invalid_dob_counts, invalid_email_pct, invalid_email_counts, invalid_country_pct, invalid_country_counts,
                   dq_score, repo_type) values (%s,%s,%s,%s, %s, %s, %s, %s, %s)""", (total, invalid_dob_pct, invalid_dob_counts, invalid_email_pct, invalid_email_counts, invalid_country_pct, invalid_country_counts,dq_avg, "phoneno"))
    
    
    conn.commit()'''
    