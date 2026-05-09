from src.extract import extract_weather_data
from src.transform import transform_weather_data
from src.load import load_to_postgres
from src.logger import get_logger

logger = get_logger(__name__)


def run_pipeline():
    try:
        logger.info('Pipeline started')
    
        # 1. Extract
        logger.info('Starting extraction')
        data = extract_weather_data()
        logger.info('Extraction complete')

        # 2. Transform
        logger.info('Starting transformation')
        df = transform_weather_data(data)
        logger.info('Transformation complete')

        # 3. Load
        logger.info('Starting load')
        load_to_postgres(df)
        logger.info('Pipeline complete')


    except Exception as e:
        logger.error(f'Pipeline failed: {e}')

if __name__ == "__main__":
    run_pipeline()