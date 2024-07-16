import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

def transfer_data():
    try:
        source_hook = PostgresHook(postgres_conn_id='source-postgres')
        target_hook = PostgresHook(postgres_conn_id='target-postgres')

        source_conn = source_hook.get_conn()
        target_conn = target_hook.get_conn()

        source_cur = source_conn.cursor()
        target_cur = target_conn.cursor()

        source_cur.execute("SELECT * FROM customers;")
        customers = source_cur.fetchall()
        
        for customer in customers:
            target_cur.execute(
                "INSERT INTO customers (id, name, email, phone, created_at) VALUES (%s, %s, %s, %s, %s);", 
                customer
            )

        target_conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Veri aktarımı sırasında hata oluştu:", error)

    finally:
        if source_conn:
            source_cur.close()
            source_conn.close()
        if target_conn:
            target_cur.close()
            target_conn.close()

with DAG(
    'postgres_transfer',
    start_date=datetime(2024, 7, 16),
    schedule='@daily',
    catchup=False
) as dag:

    transfer_task = PythonOperator(
        task_id='transfer_data',
        python_callable=transfer_data
    )
