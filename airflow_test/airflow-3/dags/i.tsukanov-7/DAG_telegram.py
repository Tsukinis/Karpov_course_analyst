from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'itsukanov',
    'depends_on_past': False,
    'retries': 0
}
dag = DAG('dag_mini_project_tsukanov',
          default_args = default_args,
          start_date = datetime(2020, 7, 15),
         schedule_interval = '0 12 * * 1')
def send_report_to_telegram():
    import pandas as pd
    import numpy as np
    import random
    
    path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR-ti6Su94955DZ4Tky8EbwifpgZf_dTjpBdiVH0Ukhsq94jZdqoHuUytZsFZKfwpXEUCKRFteJRc9P/pub?gid=889004448&single=true&output=csv'
    ads = pd.read_csv(path, parse_dates=[0])
    ads_views = ads[ads['event'] == 'view'].groupby(['date','ad_id']).count().reset_index()[['date', 'ad_id','event']]
    ads_click = ads[ads['event'] == 'click'].groupby(['date','ad_id']).count().reset_index()[['date', 'ad_id','event']]
    ads_views.columns = ['date','ad_id', 'views']
    ads_click.columns = ['date','ad_id', 'clicks']
    ads_ctr = pd.merge(ads_views, ads_click, on = ['date', 'ad_id'])
    ads_ctr['CTR'] = ads_ctr['clicks'] / ads_ctr['views']
    ads['cost_per_action'] = ads.ad_cost / 1000
    ads_ctr['money'] = ads_ctr.views * ads.cost_per_action
    money_0204 = float(ads_ctr[ads_ctr['date'] == '2019-04-02']['money'])
    views_0204 = float(ads_ctr[ads_ctr['date'] == '2019-04-02']['views'])
    clicks_0204 = float(ads_ctr[ads_ctr['date'] == '2019-04-02']['clicks'])
    ctr_0204 = float(ads_ctr[ads_ctr['date'] == '2019-04-02']['CTR'])
    money_0104 = float(ads_ctr[ads_ctr['date'] == '2019-04-01']['money'])
    views_0104 = float(ads_ctr[ads_ctr['date'] == '2019-04-01']['views'])
    clicks_0104 = float(ads_ctr[ads_ctr['date'] == '2019-04-01']['clicks'])
    ctr_0104 = float(ads_ctr[ads_ctr['date'] == '2019-04-01']['CTR'])
    diff_money = round((money_0204 - money_0104) / money_0104 * 100)
    diff_views = round((views_0204 - views_0104) / views_0104 * 100)
    diff_clicks = round((clicks_0204 - clicks_0104) / clicks_0104 * 100)
    diff_ctr = round((ctr_0204 - ctr_0104) / ctr_0104 * 100)
    message_report = f''' Отчет по объявлению 121288 за 2 апреля\n
    Траты: {money_0204} ({diff_money}%)
    Показы: {views_0204} ({diff_views}%)
    Клики: {clicks_0204} ({diff_clicks}%)
    CTR: {ctr_0204} ({diff_ctr}%)
    '''
    import requests
    import json
    from urllib.parse import urlencode

    token = '1480674807:AAGhlYdif-sCATyBBF9rpAHVPPwpJj1PBDo'
    chat_id = 166754739  # your chat id
    message = 'Отчетик прилетел'

    params = {'chat_id': chat_id, 'text': message}

    base_url = f'https://api.telegram.org/bot{token}/'
    url = base_url + 'sendMessage?' + urlencode(params)
    resp = requests.get(url)
    # Path to necessary file
    filepath = '/home/jupyter-i.tsukanov-7/airflow_test/airflow-3/dags/i.tsukanov-7/report_2019-04-02.txt'

    url = base_url + 'sendDocument?' + urlencode(params)

    files = {'document': open(filepath, 'rb')}
    resp = requests.get(url, files=files)