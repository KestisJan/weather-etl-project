import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from .logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def load_to_postgres(df):
    try:
        logger.info('Loading dotenv')
        logger.info("Start connection")
        user = os.getenv("DB_USER")
        pw = os.getenv("DB_PASSWORD")
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        db = os.getenv("DB_NAME")

        logger.info('Creating connection')
        engine = create_engine(f"postgresql://{user}:{pw}@{host}:{port}/{db}")

        with engine.begin() as conn:
            logger.info('Creating temporary staging table')
            conn.execute(text("CREATE TEMP TABLE temp_weather (LIKE weather_data INCLUDING ALL);"))

            logger.info('Streaming data to staging table')
            df.to_sql('temp_weather', conn, if_exists='append', index=False)

            logger.info('Executing Upsert (Merging staging to main table)')
            upsert_query = text("""
                INSERT INTO weather_data
                SELECT * FROM temp_weather
                ON CONFLICT (time) DO NOTHING;
            """)

            result = conn.execute(upsert_query)
            logger.info(f'Load succesful. Rows processed: {result.rowcount}')

    except Exception as e:
        logger.error(f'Load failed: {e}')
        raise