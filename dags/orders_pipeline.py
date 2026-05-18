from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mci_engineer',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'orders_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    max_active_runs=1,
    description='Orders API -> Transform -> ClickHouse'
) as dag:

    fetch_orders = BashOperator(
        task_id='fetch_orders',
        bash_command='python /opt/airflow/dags/scripts/fetch_orders.py'
    )

    transform_orders = BashOperator(
        task_id='transform_orders',
        bash_command='python /opt/airflow/dags/scripts/transform_orders.py'
    )

    load_to_clickhouse = BashOperator(
        task_id='load_to_clickhouse',
        bash_command='python /opt/airflow/dags/scripts/load_orders.py'
    )

    fetch_orders >> transform_orders >> load_to_clickhouse