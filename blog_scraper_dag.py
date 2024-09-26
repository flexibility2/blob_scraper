from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scraper import main as scraper_main

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'blog_scraper',
    default_args=default_args,
    description='A DAG to scrape blog posts',
    schedule_interval=timedelta(days=1),
)

scrape_task = PythonOperator(
    task_id='scrape_blogs',
    python_callable=scraper_main,
    dag=dag,
)

scrape_task