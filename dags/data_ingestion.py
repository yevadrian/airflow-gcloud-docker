from airflow import DAG
from airflow.decorators import task
from google.cloud import storage, bigquery
from datetime import datetime
import pandas as pd
import requests
import json

with DAG(dag_id='data_ingestion', start_date=datetime.now(), schedule='@once'):

    @task
    def call_dataset():
        data = requests.get('https://datausa.io/api/data?drilldowns=Nation&measures=Population').content
        data = json.loads(data)
        with open('outputs/data.json', 'w') as file:
            json.dump(data, file)

    @task
    def save_as_csv():
        with open('outputs/data.json', 'r') as file:
            data = json.load(file)
        df = pd.json_normalize(data, record_path=['data'])
        df.to_csv('outputs/data.csv', index=False)

    @task
    def format_to_parquet():
        df = pd.read_csv('outputs/data.csv')
        df.to_parquet('outputs/data.parquet')

    @task
    def local_to_gcs():
        client = storage.Client()
        bucket = client.get_bucket('data-fellowship-8-yevadrian')
        blob = bucket.blob('data.parquet')
        blob.upload_from_filename('outputs/data.parquet')

    @task
    def bigquery_external_table():
        client = bigquery.Client()
        client.create_dataset('data_fellowship', exists_ok=True)
        dataset = client.dataset('data_fellowship')

        external_config = bigquery.ExternalConfig('PARQUET')
        external_config.autodetect = True
        external_config.source_uris = ['gs://data-fellowship-8-yevadrian/data.parquet']

        table_ref = bigquery.TableReference(dataset, 'population')
        table = bigquery.Table(table_ref, schema=None)
        table.external_data_configuration = external_config
        client.create_table(table, exists_ok=True)
    
    call_dataset() >> save_as_csv() >> format_to_parquet() >> local_to_gcs() >> bigquery_external_table()