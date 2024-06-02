import psycopg2

DB_NAME = 'bmi'
DB_USER = 'postgres'
DB_PASSWORD = 'Mrpl123$'
DB_HOST = 'localhost'

def connect_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
   
    return conn

conn = connect_db() 
if conn:
    print('Connected to the database')
elif not conn:
    print('Not connected to the database')