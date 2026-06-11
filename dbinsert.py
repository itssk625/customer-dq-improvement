import psycopg2 as psy
import pandas as pd
from psycopg2.extras import execute_values
try:
    conn=psy.connect(
    host="localhost",
    database="customerdqproject",
    user="postgres",
    password="itsjustme",
    port="5432"
    )
    print("Successful")
    cursor=conn.cursor()

    df = pd.read_sql("SELECT * FROM stage_monoprix.users limit 20", conn)
    print(df)

    print(f"Read {len(df)} rows successfully")
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:  
    print("Connection failed")
    print(e)



