import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

DB_HOST = 'localhost'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'Abcd@1234'
DB_NAME = 'Diabetic'

def main():
    try:
        # Connect to default 'postgres' database to create DB if needed
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname='postgres', user=DB_USER, password=DB_PASSWORD)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
        exists = cur.fetchone()
        if not exists:
            print(f"Creating database {DB_NAME}...")
            cur.execute('CREATE DATABASE "' + DB_NAME + '"')
        else:
            print(f"Database {DB_NAME} already exists")
        cur.close()
        conn.close()
    except Exception as e:
        print('Error connecting to postgres to create DB:', e)
        sys.exit(1)

    # Connect to the target database and create users table
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(30),
            password VARCHAR(255) NOT NULL
        );
        '''
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        conn.close()
        print('users table ensured in database', DB_NAME)
    except Exception as e:
        print('Error creating users table:', e)
        sys.exit(1)

if __name__ == '__main__':
    main()
