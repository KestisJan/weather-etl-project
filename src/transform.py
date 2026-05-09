import pandas as pd
from datetime import datetime
from .logger import get_logger

logger = get_logger(__name__)


def transform_weather_data(raw_data):
    try:
        logger.info('Transformation started')
        current = raw_data.get('current_weather')
        df = pd.DataFrame([current])
        logger.info('Converting datetime')
        df['time'] = pd.to_datetime(df['time'])
        df['processed_at'] = datetime.now()
        logger.info('Transformation complete')
        return df
    except Exception as e:
        logger.error(f'Transformation failed: {e}')
        raise