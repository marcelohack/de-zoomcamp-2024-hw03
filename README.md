
# Data Engineering Zoomcamp 2024 - Homework 3

## Instructions

### 1 - Create Docker/Postgres data folder:

```console
mkdir -p data/postgres
```
### 2 - Start Airflow/Docker:

- Adjust the airflow/docker-compose.yaml file with the right GCP Project ID, credentials, Cloud Storage bucket name, etc.

```console
docker compose -f airflow/docker-compose.yaml up -d
```

### 3 - Data Ingestion

Open the browser, then go to Airflow on http://localhost:8080, (credentials: airflow/airflow), run the dag: data_ingestion_gcs_dag

### 4 - GCP / Cloud Storage
Go to the GCP console, navigate to the de-zoomcamp project
Check the Cloud Storage de-zoomcamp-data-lake Bucket, check the folder raw/green/2022, you should see the parquet files

### 5 - GCP / BigQuery - External Table

For creating the BigQuery - External Table
You can run the gcp_stack Terraform or create the External Table from the GCP / BigQuery console

#### 5.1 - Terraform
- Adjust the gcp_stack/variables.tf file with the right GCP Project ID, credentials, Cloud Storage bucket name, BigQuery dataset, table name, etc.
- Execute the following steps:

```console
cd gcp_stack
terraform init 
terraform apply
```

> The **terraform destroy** command won't drop BigQuery the External Table, because the resource was created with the attribute deletion_protection=true (default), if you want to make it destroyable, create the resource with the attribute deletion_protection=false

#### 5.2 - BigQuery console

From the BigQuery console, execute the following instruction:

```console
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp.trips_dataset.trips_green_2022_external`
OPTIONS (
    format ="PARQUET",
    uris = ['gs://<bucket_name>/raw/green/2022/*.parquet']
);
```

### 6 - GCP / BigQuery - Materialized Table

From the BigQuery console, execute the following instruction:

```console
CREATE OR REPLACE TABLE `de-zoomcamp.trips_dataset.trips_green_2022_materialized` AS 
SELECT * FROM `de-zoomcamp.trips_dataset.trips_green_2022_external`;
```

### 7 - Questions  
Please check the [Homework Execution](./homework_execution.md) document.

### 8 - Stop Airflow/Docker

```console
docker compose -f airflow/docker-compose.yaml down -v
```