import requests
from .logger import get_logger
import time

logger = get_logger(__name__)



def extract_weather_data():
    logger.info('Extraction started')
    url = "https://api.open-meteo.com/v1/forecast?latitude=54.90&longitude=23.90&current_weather=true&hourly=temperature_2m,windspeed_10m,weathercode&forecast_days=1"
    # url = "https://api.open-meteo.com/v1/BROKEN_URL"

    max_attempts = 3
    base_delay = 5

    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f'Attempt {attempt} of {max_attempts}')
            response = requests.get(url, timeout=10)
            response.raise_for_status() # raises error if status code is 4xx or 5xx

            logger.info('Extraction successful')
            return response.json()
        
        except requests.exceptions.ConnectionError:
            logger.error(f'Attempt {attempt} failed - API uncreachable')
            if attempt < max_attempts:
                delay = base_delay * (2 ** (attempt - 1))
                logger.info(f'Retrying in {delay} seconds...')
                time.sleep(delay)
            else:
                logger.error('All attempts exhausted')
                raise

        except requests.exceptions.HTTPError as e:
            if response.status_code >= 500:
                if attempt < max_attempts:
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning(f'Server error {response.status_code}. Retrying in {delay}s...')
                    time.sleep(delay)
                    continue

            logger.error(f'Bad API response: {e}')
            raise
        
        except Exception as e:
            logger.error('Unexpected error: {e}')
            raise
