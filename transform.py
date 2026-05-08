import pandas as pd
from datetime import datetime

def transform_weather_data(raw_data):
    current = raw_data.get('current_weather')
    df = pd.DataFrame([current])
    df['time'] = pd.to_datetime(df['time'])
    df['processed_at'] = datetime.now()
    return df