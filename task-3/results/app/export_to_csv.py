import os

import psycopg2


def export_table_to_csv():
    host = os.getenv('POSTGRES_HOST')
    port = os.getenv('POSTGRES_PORT')
    password = os.getenv('POSTGRES_PASSWORD')
    user = os.getenv('POSTGRES_USER')
    dbname = os.getenv('POSTGRES_DATABASE')
    table_name = os.getenv('EXPORT_TABLE_NAME')
    csv_file_path = os.getenv('OUTPUT_FILE')

    print(f"Connecting to PostgreSQL at {host}:{port}")

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cur = conn.cursor()
    with open(csv_file_path, 'w') as f:
        sql = f"COPY {table_name} TO STDOUT WITH CSV HEADER DELIMITER ';'"
        cur.copy_expert(sql, f)
    cur.close()
    conn.close()
    print(f"Таблица {table_name} экспортирована в {csv_file_path}")

export_table_to_csv()
