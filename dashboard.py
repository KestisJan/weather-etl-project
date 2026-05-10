import os
import pandas as pd
import time
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

WEATHER_CODES = {
    0: 'Clear Sky',
    1: 'Mainly Clear',
    2: 'Partly Cloudy',
    3: 'Overcast',
    45: 'Foggy',
    48: 'Icy Fog',
    51: 'Light Drizzle',
    53: 'Moderate Drizzle',
    55: 'Dense Drizzle',
    61: 'Slight Rain',
    63: 'Moderate Rain',
    65: 'Heavy Rain',
    71: 'Slight Snow',
    73: 'Moderate Snow',
    75: 'Heavy Snow',
    80: 'Slight Showers',
    81: 'Moderate Showers',
    82: 'Heavy Showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with Hail',
    99: 'Thunderstorm with Heavy Hail'
}

load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
df = pd.read_sql('SELECT * FROM hourly_weather_data ORDER BY time', engine)
df['weather_description'] = df['weathercode'].map(WEATHER_CODES)
latest = df.iloc[-1]

st.title('Weather Dashboard - Kaunas')
temp_delta = round(latest['temperature'] - df.iloc[-2]['temperature'], 1)

col1, col2, col3 = st.columns(3)
col1.metric(label='Temperature', value=f"{latest['temperature']}°C", delta=f"{temp_delta}°C")
col2.metric(label='Windspeed', value=f"{latest['windspeed']} km/h")
col3.metric(label='Condition', value=WEATHER_CODES.get(int(latest['weathercode']), 'Unknown'))

hours = df['time'].dt.hour.tolist()
min_hour, max_hour = st.select_slider(
    'Select hour range',
    options=hours,
    value=(hours[0], hours[-1])
)

df_filtered = df[(df['time'].dt.hour >= min_hour) & (df['time'].dt.hour <= max_hour)]

st.subheader('Temperature over time')
st.line_chart(df_filtered.set_index('time')['temperature'])

st.subheader('Windspeed over time')
st.line_chart(df_filtered.set_index('time')['windspeed'])

st.divider()


col4, col5, col6 = st.columns(3)
col4.metric(label='Max Temperature', value=f"{df['temperature'].max()}°C")
col5.metric(label='Min Temperature', value=f"{df['temperature'].min()}°C")
col6.metric(label='Avg Windspeed', value=f"{df['windspeed'].mean():.1f} km/h")

time.sleep(60)
st.rerun()

