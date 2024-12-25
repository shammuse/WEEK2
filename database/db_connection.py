import psycopg2

conn = psycopg2.connect(
    dbname="telecom_data",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("SELECT version();")
print(cursor.fetchone())

cursor.close()
conn.close()
