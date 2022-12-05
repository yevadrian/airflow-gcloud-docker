### Ingest data to Google Cloud Storage and Google BigQuery with Apache Airflow on Docker.

##### Modify "key.json" according to your Google service account credentials.
> nano key.json

##### Modify the DAG according to your needs.
> nano dags/data_ingestion.py

Create Airflow stacks with Docker Compose.
> sudo docker compose up -d

##### Open Airflow with username "airflow" and password "airflow" then run the DAG.
> localhost:8080
