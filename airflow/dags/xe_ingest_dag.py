from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

import requests
import pandas as pd
import json
from datetime import date, datetime
import os
from dotenv import load_dotenv
load_dotenv()

def fetch_data(base_url, endpoint, params, ti):
    auth = {
        'user': os.getenv('API_ID'),
        'password': os.getenv('API_KEY')
    }
    params.update(auth)
    r = requests.get(f'{base_url}/{endpoint}/', auth=(auth['user'], auth['password']), params=params)
    print(r)
    
    ti.xcom_push(key='xe_data', value=r.json())
    # return r.json()

def convert_to_dataframe(today, home_dir, ti):
    json_data = ti.xcom_pull(key='xe_data', task_ids='fetch_xe_data_task')
    
    df = pd.DataFrame()
    quotecurrency = []
    mid = []
    inverse = []
    for idx in json_data['to']:
        quotecurrency.append(idx['quotecurrency'])
        mid.append(idx['mid'])
        inverse.append(idx['inverse'])
    df['USD_to_currency_rate'] = mid
    df['currency_to_USD_rate'] = inverse
    df['currency_to'] = quotecurrency
    df['timestamp'] = json_data['timestamp']
    df['currency_from'] = json_data['from']
    columns = ['timestamp', 'currency_from', 'USD_to_currency_rate', 'currency_to_USD_rate', 'currency_to']
    df = df[columns]

    df.to_csv(f'results/rates_{today}.csv', index=0)

    # return df

# def xe_pipeline(base_url, endpoint, params):
#     convert_from = fetch_data(base_url=base_url, endpoint=endpoint, params=params)
#     result = convert_to_dataframe(convert_from)
#     result.to_csv(f'rates_{today}.csv', index=0)


home_dir = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
today = date.today()
base_url = 'https://xecdapi.xe.com/v1'
ops = {
    'from': 'USD',
    'to': ','.join(['NGN', 'GHS', 'KES', 'UGX', 'MAD', 'XOF', 'EGP']),
    'amount': 1,
    # 'obsolete': False,
    'inverse': True
}

default_args = {
    "owner": "autochek",
    "start_date": datetime(2022, 8, 21),
    "depends_on_past": False,
    "retries": 1,
}

#################### Morning Run #####################

dag_1 = DAG(
    dag_id="xe_ingest_morning",
    schedule_interval="0 1 * * *",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['auto'],
)

with dag_1:
    fetch_data_task = PythonOperator(
        task_id = 'fetch_xe_data_task',
        python_callable=fetch_data,
        op_kwargs={
            'base_url': base_url, 
            'endpoint': 'convert_from', 
            'params': ops
        }
    )

    convert_to_df = PythonOperator(
        task_id = 'convert_json_to_df_task',
        python_callable=convert_to_dataframe,
        op_kwargs={
            'today': today,
            'home_dir': home_dir
        }
    )

    fetch_data_task >> convert_to_df

################# Evening run ######################

dag_2 = DAG(
    dag_id="xe_ingest_evening",
    schedule_interval="0 23 * * *",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['auto'],
)

with dag_2:
    fetch_data_task_evening = PythonOperator(
        task_id = 'fetch_xe_data_task',
        python_callable=fetch_data,
        op_kwargs={
            'base_url': base_url, 
            'endpoint': 'convert_from', 
            'params': ops
        }
    )

    convert_to_df_task_evening = PythonOperator(
        task_id = 'convert_json_to_df_task',
        python_callable=convert_to_dataframe,
        op_kwargs={
            'today': today,
            'home_dir': home_dir
        }
    )

    fetch_data_task_evening >> convert_to_df_task_evening