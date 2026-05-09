import os
import pandas as pd
import time
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
df = pd.read_sql('SELECT * FROM weather_data ORDER BY time', engine)
latest = df.iloc[-1]

st.title('Weather Dashboard - Kaunas')

col1, col2 = st.columns(2)
col1.metric(label='Temperature', value=f"{latest['temperature']}°C")
col2.metric(label='Windspeed', value=f"{latest['windspeed']} km/h")

st.subheader('Temperature over time')
st.line_chart(df.set_index('time')['temperature'])

st.subheader('Windspeed over time')
st.line_chart(df.set_index('time')['windspeed'])

time.sleep(60)
st.rerun()

