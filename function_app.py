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
    acc_name = "smogwatchstorage1"
    acc_key = os.environ['STORAGE_ACCOUNT_KEY']
    
    try:
        # extracting rates data
        r = requests.get("https://api.nbp.pl/api/exchangerates/tables/A/")
        data = r.json()[0]
        df = pd.DataFrame(data['rates'])
        df['effectiveDate'] = data['effectiveDate']
        df['load_date'] = today

        # loading raw rates data
        path = f"abfss://bronze@{acc_name}.dfs.core.windows.net/nbp/rates/date={today}/data.parquet"
        df.to_parquet(path, storage_options={'account_name': acc_name, 'account_key': acc_key})

        # extracting gold data
        r_gold = requests.get("https://api.nbp.pl/api/cenyzlota")
        g_data = r_gold.json()[0]
        df_gold = pd.DataFrame([{'date': g_data['data'], 'price': g_data['cena'], 'load_date': today}])

        # loading raw gold data
        path_g = f"abfss://bronze@{acc_name}.dfs.core.windows.net/nbp/gold/date={today}/data.parquet"
        df_gold.to_parquet(path_g, storage_options={'account_name': acc_name, 'account_key': acc_key})
        
    except Exception as e:
        print(f"Extraction failed: {e}")
