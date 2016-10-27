from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pprint import pprint

from a_prepare_image_set import PrepareImages
from b_create_vocabulary import Vocabulary

default_args = {
    'owner': 'styleio',
    'depends_on_past': False,
    'start_date': datetime(2016, 10, 20),
    'email': ['andreas@styleio.se'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'schedule_interval': '@once'
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('styleio_training', default_args=default_args)

# tasks for operators
def prep_images(**kwargs):
    print "arguments", kwargs['imgdir']
    #print "arguments", kwargs
    prepIm = PrepareImages(path=kwargs['imgdir'])
    prepIm.imagePrep()
    return 'Prepared images'


def create_vocab(**kwargs):
    voc = Vocabulary(imgs_path=kwargs['imgdir'], vocab_size = 800, feature_type='daisy')
    all_features = voc.feature_extraction()
    voc.create_vocabulary(all_features)
    voc.save_vocabulary()
    return 'Created vocabulary'

def create_vocab(**kwargs):
    ph = PatternHistograms(path=kwargs['imgdir'], feature_type='daisy')
    hists = ph.create_histogram()
    ph.save_histograms(hists)
    return 'Created vocabulary'

create_temp_folder = """
echo "Create folder"
mkdir {{params.imgdir}}_new
"""

delete_temp_folder = """
rm -r {{params.imgdir}}_new
"""

# operator definition
image_preparation = PythonOperator(
    task_id='image_preparation',
    provide_context=True,
    python_callable=prep_images,
    op_kwargs={'imgdir': 'wallpapers'},
    dag=dag)

create_vocabulary = PythonOperator(
    task_id='create_vocabulary',
    provide_context=True,
    python_callable=create_vocab,
    op_kwargs={'imgdir': 'wallpapers'},
    dag=dag)


create_temporary_image_directory = BashOperator(
    task_id='create_dir',
    bash_command=create_temp_folder,
    params={'imgdir': 'wallpapers'},
    dag=dag)


delete_temporary_image_directory = BashOperator(
    task_id='delete_dir',
    bash_command=delete_temp_folder,
    params={'imgdir': 'wallpapers'},
    dag=dag)

image_preparation.set_upstream(create_temporary_image_directory)
create_vocabulary.set_upstream(image_preparation)
delete_temporary_image_directory.set_upstream(create_vocabulary)

