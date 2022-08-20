import requests
import pandas as pd
import json
from datetime import date
import os
from dotenv import load_dotenv
load_dotenv()


def fetch_data(base_url, endpoint, params):
    auth = {
        'user': os.getenv('API_ID'),
        'password': os.getenv('API_KEY')
    }
    params.update(auth)
    r = requests.get(f'{base_url}/{endpoint}/', auth=(auth['user'], auth['password']), params=params)
    print(r)
    
    return r.json()


def convert_to_dataframe(json_data):
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

    return df

if __name__ == '__main__':
    today = date.today()
    base_url = 'https://xecdapi.xe.com/v1'
    ops = {
        'from': 'USD',
        'to': ','.join(['NGN', 'GHS', 'KES', 'UGX', 'MAD', 'XOF', 'EGP']),
        'amount': 1,
        # 'obsolete': False,
        'inverse': True
    }
    convert_from = fetch_data(base_url=base_url, endpoint='convert_from', params=ops)

    result = convert_to_dataframe(convert_from)
    result.to_csv(f'rates_{today}.csv', index=0)
