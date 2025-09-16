import smtplib
from datetime import timedelta
from email.mime.text import MIMEText

import pandas as pd
import psycopg2
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.trigger_rule import TriggerRule

success_email = Variable.get("success_email")
failure_email = Variable.get("failure_email")
smtp_password = Variable.get("smtp_password")
smtp_server = Variable.get("smtp_server")
smtp_port = Variable.get("smtp_port")
airflow_postgres_password = Variable.get("airflow_postgres_password")

# Опции для DAG: retry и уведомления по email
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': [success_email],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}


# Функция чтения из PostgreSQL
def read_from_postgres():
    conn = psycopg2.connect(
        dbname='postgres',
        user='airflow',
        password=airflow_postgres_password,
        host='postgres',
        port='5432'
    )
    query = "SELECT status FROM orders LIMIT 10;"
    df = pd.read_sql(query, conn)
    conn.close()
    print(df)
    # Сохраняем для передачи в XCom
    return df['status'].tolist()


# Функция чтения из CSV
def read_from_csv():
    df = pd.read_csv('/opt/airflow/data/orders.csv')
    print(df.head())
    return df.shape[0]


# Функция ветвления по условию
def branch_by_data(ti):
    statuses = ti.xcom_pull(task_ids='read_postgres')
    if 'delivered' in statuses:
        return 'process_delivered'
    else:
        return 'process_other'

# Обработка в "ветке delivered"
def process_delivered():
    print("Processing delivered orders")

# Обработка в "остальной" ветке
def process_other():
    print("Processing other orders")

def send_success_email():
    print("Start send_success_email")
    body = "Success email sent from Airflow worker using smtplib."
    send_email(success_email, body)

def send_error_email(context):
    print("Start send_error_email")
    body = "Error email sent from Airflow worker using smtplib."
    send_email(failure_email, body)

def send_email(email_to, body) :
    USERNAME = email_to
    PASSWORD = smtp_password

    sender_email = USERNAME
    subject = "Test Email from Airflow Worker"

    # Создаем email сообщение
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email_to

    try:
        # Подключаемся к SMTP серверу с SSL
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(sender_email, email_to, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# DAG объявление
with DAG(
        dag_id='poc_etl_pipeline',
        default_args=default_args,
        description='ETL pipeline with branching, retry and email notifications',
        schedule='@daily',
        catchup=False,
) as dag:
    # Чтение из PostgreSQL
    read_postgres = PythonOperator(
        task_id='read_postgres',
        python_callable=read_from_postgres,
        retries=3,
        retry_delay=timedelta(seconds=10),
        on_failure_callback=send_error_email
    )

    # Чтение из CSV
    read_csv = PythonOperator(
        task_id='read_csv',
        python_callable=read_from_csv,
        retries=3,
        retry_delay=timedelta(minutes=2)
    )

    # Ветвление по условию
    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=branch_by_data,
        retries=2,
    )

    # Задачи обработки веток
    process_delivered_task = PythonOperator(
        task_id='process_delivered',
        python_callable=process_delivered
    )

    process_other_task = PythonOperator(
        task_id='process_other',
        python_callable=process_other
    )

    # Email при успешном выполнении пайплайна
    process_success_email = PythonOperator(
        task_id='process_success_email',
        python_callable=send_success_email,
        trigger_rule=TriggerRule.NONE_FAILED,
    )

#    process_error_email = PythonOperator(
#        task_id='process_error_email',
#        python_callable=send_error_email
#    )

    # Определение порядка шагов
    [read_postgres, read_csv] >> branching >> [process_delivered_task, process_other_task] >> process_success_email
    #branching >> [process_delivered_task, process_other_task] >> process_success_email
    #[read_postgres, branching, process_delivered_task, process_other_task] >> process_error_email

