import os

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from google.cloud import storage

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

dataset_url_template = "https://d37ci6vzurychx.cloudfront.net/trip-data/{}_tripdata_{}-{}.parquet"

path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

def download_datasets(color, year, **kwargs):
    for month in range(1, 13):
        month = str(month).zfill(2)
        file_key = f"{color}_tripdata_{year}-{month}.parquet"
        local_file = f"{path_to_local_home}/{file_key}"
        dataset_url = dataset_url_template.format(color, year, month)
        print(f"Downloading {dataset_url} to {local_file}")
        os.system(f"curl -sSL {dataset_url} > {local_file}")
        ti = kwargs['ti'] # Task Instance
        ti.xcom_push(key=f'file_key_{month}', value=file_key)
        ti.xcom_push(key=f'local_file_{month}', value=local_file)

# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, color, year, **kwargs):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    ti = kwargs['ti'] # Task Instance

    for month in range(1, 13):
        month = str(month).zfill(2)
        file_key = ti.xcom_pull(key=f'file_key_{month}', task_ids='download_datasets_task')
        local_file = ti.xcom_pull(key=f'local_file_{month}', task_ids='download_datasets_task')

        object_name = f"raw/{color}/{year}/{file_key}"

        print(f"Uploading {local_file} to gs://{bucket.name}/{object_name}")

        blob = bucket.blob(object_name)
        blob.upload_from_filename(local_file)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

default_params = {
    "taxi_color": "green",
    "datasets_year": 2022,
}

with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    params = default_params,
    catchup=False,
    max_active_runs=1,
    tags=['dtc-de'],
) as dag:

    download_datasets_task = PythonOperator(
        task_id="download_datasets_task",
        python_callable=download_datasets,
        op_kwargs={
            "color": "{{ dag_run.conf['taxi_color'] }}",
            "year": "{{ dag_run.conf['datasets_year'] }}",
        },
    )

    upload_to_gcs_task = PythonOperator(
        task_id="upload_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "color": "{{ dag_run.conf['taxi_color'] }}",
            "year": "{{ dag_run.conf['datasets_year'] }}",
        },
    )

    download_datasets_task >> upload_to_gcs_task
