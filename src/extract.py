import requests
from .logger import get_logger

logger = get_logger(__name__)

def extract_weather_data():
    logger.info('Extraction started')
    url = "https://api.open-meteo.com/v1/forecast?latitude=54.90&longitude=23.90&current_weather=true&hourly=temperature_2m,windspeed_10m,weathercode&forecast_days=1"

    try:
        response = requests.get(url)
        response.raise_for_status() # raises error if status code is 4xx or 5xx
        logger.info('Extraction successful')
        return response.json()
    except requests.exceptions.ConnectionError:
        logger.error('API unreachable - check internet connection')
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f'Bad API response: {e}')
        raise