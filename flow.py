from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pprint import pprint


default_args = {
    'owner': 'styleio',
    'depends_on_past': False,
    'start_date': datetime(2016, 6, 1),
    'email': ['andreas@styleio.se'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('styleio-training', default_args=default_args)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

image_preparation = PythonOperator(
    task_id='image_preparation',
    provide_context=True,
    python_callable=print_context,
    dag=dag)

create_vocabulary = PythonOperator(
    task_id='image_preparation',
    provide_context=True,
    python_callable=print_context,
    dag=dag)


temporary_image_directory = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

image_preparation.set_upstream(temporary_image_directory)
create_vocabulary.set_upstream(image_preparation)
