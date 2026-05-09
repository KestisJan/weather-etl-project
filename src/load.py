import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from .logger import get_logger

logger = get_logger(__name__)

def load_to_postgres(df):
    try:
        logger.info('Loading dotenv')
        load_dotenv()
        logger.info("Start connection")
        user = os.getenv("DB_USER")
        pw = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db = os.getenv("DB_NAME")
        logger.info('Creating connection')
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")
        df.to_sql('weather_data', engine, if_exists='append', index=False)
        logger.info('Load succesful.')
    except Exception as e:
        logger.error(f'Load failed: {e}')
        raise