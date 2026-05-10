import pandas as pd
from datetime import datetime
from .logger import get_logger
from .schemas import HourlyWeather

logger = get_logger(__name__)


def transform_weather_data(raw_data):
    try:
        logger.info('Transformation started')
        hourly = raw_data.get('hourly')

        logger.info('Data validation')
        validated_hourly = HourlyWeather(**hourly)

        logger.info('Converting validated model to Dataframe')
        df_hourly = pd.DataFrame({
            'time': validated_hourly.time,
            'temperature': validated_hourly.temperature_2m,
            'windspeed': validated_hourly.windspeed_10m,
            'weathercode': validated_hourly.weathercode
        })

        logger.info('Converting datetime')
        df_hourly['time'] = pd.to_datetime(df_hourly['time'])
        df_hourly['processed_at'] = datetime.now()

        logger.info('Transformation complete')
        return df_hourly

    except Exception as e:
        logger.error(f'Transformation failed: {e}')
        raise