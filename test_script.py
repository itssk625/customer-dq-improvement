from db.connection import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
INSERT INTO raw_customer_records
(
    file_id,
    first_name,
    last_name,
    dob,
    country,
    gender,
    email,
    phone_no
)
VALUES
(
    'test1',
    'John',
    'Doe',
    '01-01-2000',
    'India',
    'Male',
    'john@gmail.com',
    '+91 9876543210'
)
""")

conn.commit()

print("Inserted!")

cur.close()
conn.close()