from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='investing_data_pipeline',
    default_args=default_args,
    description='Pipeline diário de ingestão de dados econômicos',
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_etl = BashOperator(
    task_id='run_etl',
    bash_command='python /opt/airflow/dags/scripts/load_data.py'
)