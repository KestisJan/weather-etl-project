from extract import extract_weather_data
from transform import transform_weather_data
from load import load_to_postgres

def run_pipeline():
    # 1. Get raw data from API
    data = extract_weather_data()

    # 2. Clean and format with Pandas
    df = transform_weather_data(data)

    # 3. Save to PostgreSQL
    load_to_postgres(df)

    print('ETL complete.')

if __name__ == "__main__":
    run_pipeline()