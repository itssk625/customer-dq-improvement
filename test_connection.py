from db.connection import get_connection
conn=get_connection()
print("Connected")
cur=conn.cursor()
cur.execute("select current_database();")
print(cur.fetchone())
cur.close()
conn.close()