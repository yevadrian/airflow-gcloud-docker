## Upload remote files to your Google Cloud Storage with Google Cloud SDK on Docker.

##### Modify "key.json" according to your Google service account credentials.
> nano key.json

##### Modify the DAG according to your needs.
> nano dags/data_ingestion.py

Create Airflow stacks with Docker Compose.
> sudo docker compose up

##### Open Airflow in your web browser and run the DAG.
> [localhost:8080](https://localhost:8080)
