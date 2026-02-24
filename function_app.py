import azure.functions as func
import os
import pandas as pd
import requests
from datetime import date

app = func.FunctionApp()

#  every 5min from the national poland bank
@app.timer_trigger(schedule="0 */5 * * * *", arg_name="timer")
def NBPExtract(timer: func.TimerRequest):
    today = date.today().isoformat()
    name = "smogwatchstorage1"
    key = os.environ['STORAGE_ACCOUNT_KEY']
    
    try:
        # exchange rates
        r = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = r.json()[0]
        df = pd.DataFrame(data['rates'])
        df['load_date'] = today
        df['effectiveDate'] = data['effectiveDate']

        # into bronze container
        path = f"abfss://bronze@{name}.dfs.core.windows.net/nbp/rates/date={today}/data.parquet"
        df.to_parquet(path, storage_options={'account_name': name, 'account_key': key})

        # gold price
        r_gold = requests.get("https://api.nbp.pl/api/cenyzlota")
        gold_data = r_gold.json()[0]
        df_gold = pd.DataFrame([{'date': gold_data['data'], 'price': gold_data['cena'], 'load_date': today}])

        path_gold = f"abfss://bronze@{name}.dfs.core.windows.net/nbp/gold/date={today}/data.parquet"
        df_gold.to_parquet(path_gold, storage_options={'account_name': name, 'account_key': key})
        
    except Exception:
        print(f"Extraction failed:")
