# Weather ETL Pipeline

A modular, production-inspired data engineering pipeline that automates the extraction, transformation, and storage of real-time hourly weather data for Kaunas, Lithuania.

---

## Overview

This project demonstrates a professional ETL architecture built with Python and PostgreSQL. Hourly weather forecasts are fetched from the Open-Meteo API, validated with Pydantic, cleaned and normalized with Pandas, and persisted into a containerized PostgreSQL database — with full logging, error handling, and deduplication at every stage. A live Streamlit dashboard visualizes the data in real time.

---

## Features

- **Extract** — Stateless GET requests to the Open-Meteo API, retrieving 24-hour hourly forecast data with retry-safe error handling
- **Transform** — JSON-to-DataFrame conversion, UTC datetime normalization, and `processed_at` metadata injection for auditability
- **Load** — Staging table + upsert pattern to PostgreSQL via SQLAlchemy, preventing duplicate records on every run
- **Data Validation** — Pydantic schema validation prevents corrupt or malformed API data from reaching the database
- **Deduplication** — `ON CONFLICT (time) DO NOTHING` upsert ensures idempotency across pipeline runs
- **Logging** — Simultaneous console and file logging with structured format across all pipeline stages
- **Error Handling** — Per-stage exception handling with descriptive error messages and graceful failure
- **Containerized Database** — PostgreSQL 15 running in Docker with persistent volume storage
- **Full Docker Stack** — Single `docker compose up` starts database and runs pipeline automatically
- **Secure Configuration** — Decoupled credentials via `.env` files, never committed to version control
- **Rich Dashboard** — Interactive Streamlit dashboard with hour range slider, weather descriptions, and delta metrics

---

## Tech Stack

| Category | Tool |
|---|---|
| Language | Python 3.x |
| Data Processing | Pandas |
| Data Validation | Pydantic |
| HTTP Client | Requests |
| ORM | SQLAlchemy |
| Database Driver | Psycopg2 |
| Database | PostgreSQL 15 |
| Dashboard | Streamlit |
| Containerization | Docker, Docker Compose |
| Environment | Python-dotenv |
| Version Control | Git |

---

## Project Structure

```
weather-etl-project/
├── src/
│   ├── __init__.py
│   ├── extract.py        # API connection and raw data retrieval
│   ├── transform.py      # Data cleaning, validation and normalization
│   ├── load.py           # Database connection, staging and upsert
│   ├── logger.py         # Centralized logging configuration
│   └── schemas.py        # Pydantic models for data validation
├── logs/
│   └── pipeline.log      # Pipeline execution logs
├── .env                  # Local credentials (not committed)
├── .env.local            # Local development credentials
├── .env.example          # Credential template for new contributors
├── .gitignore
├── Dockerfile            # Python ETL container definition
├── docker-compose.yml    # Full stack service definition
├── dashboard.py          # Streamlit weather dashboard
├── main.py               # Pipeline orchestrator
├── requirements.txt      # Pinned Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.x
- Docker and Docker Compose
- Git

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd weather-etl-project
```

### 2. Configure environment variables

Copy the example file and fill in your credentials:

```bash
cp .env.example .env
```

```ini
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
```

### 3. Launch the database

Start the PostgreSQL container in detached mode:

```bash
docker compose up -d
```

### 4. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

### Option A — Local Python + Docker database

```bash
docker compose up -d
export $(cat .env.local | xargs) && python main.py
```

### Option B — Full Docker stack (database + pipeline)

```bash
docker compose up --build
```

Single command starts everything automatically.

### Expected log output

```
2026-05-10 08:48:25 | INFO     | main       | Pipeline started
2026-05-10 08:48:25 | INFO     | main       | Starting extraction
2026-05-10 08:48:25 | INFO     | extract    | Extraction started
2026-05-10 08:48:25 | INFO     | extract    | Extraction successful
2026-05-10 08:48:25 | INFO     | main       | Extraction complete
2026-05-10 08:48:25 | INFO     | main       | Starting transformation
2026-05-10 08:48:25 | INFO     | transform  | Transformation started
2026-05-10 08:48:25 | INFO     | transform  | Data validation
2026-05-10 08:48:25 | INFO     | transform  | Converting validated model to DataFrame
2026-05-10 08:48:25 | INFO     | transform  | Transformation complete
2026-05-10 08:48:25 | INFO     | main       | Starting load
2026-05-10 08:48:25 | INFO     | load       | Creating temporary staging table
2026-05-10 08:48:25 | INFO     | load       | Executing Upsert
2026-05-10 08:48:25 | INFO     | load       | Load successful. Rows processed: 24
2026-05-10 08:48:25 | INFO     | main       | Pipeline complete
```

### Verify data in database

```bash
docker exec -it weather_postgres psql -U myuser -d weather_db -c "SELECT * FROM hourly_weather_data;"
```

---

## Dashboard

To launch the live weather dashboard:

```bash
export $(cat .env.local | xargs) && streamlit run dashboard.py
```

Opens at `http://localhost:8501` — auto refreshes every 60 seconds.

### Dashboard Features

- Current temperature with delta from previous hour
- Current windspeed and human-readable weather condition
- Interactive hour range slider — zoom into specific hours
- Temperature line chart
- Windspeed line chart
- Min/Max temperature and average windspeed for the day
- Weather conditions bar chart per hour

---

## Data Pipeline Architecture

### Staging & Upsert Logic

To ensure data integrity and prevent duplicate records, this project implements a **Staging + Upsert** pattern:

1. **Extraction** — Fetches 24-hour hourly forecast from Open-Meteo API
2. **Validation** — Pydantic validates every field type before transformation
3. **Staging** — Data is loaded into a PostgreSQL `TEMP TABLE`
4. **Upsert** — Data is merged into the main table using `ON CONFLICT (time) DO NOTHING`

If the pipeline runs multiple times within the same hour — existing records are skipped, no duplicates created.

---

## Reliability & Observability

### Error Handling

| Stage | Failure Scenario | Behaviour |
|---|---|---|
| Extract | API unreachable | Logs error, raises exception, pipeline stops |
| Extract | Bad HTTP response (4xx/5xx) | Logs status code, raises exception |
| Transform | Schema validation failure | Pydantic logs field errors, raises exception |
| Transform | Malformed data | Logs error, raises exception |
| Load | Database unreachable | Logs error, raises exception, no partial writes |

### Logging

All pipeline activity is logged simultaneously to the console and `logs/pipeline.log`.

**Log format:**
```
timestamp | level | module | message
```

**Log levels used:**

| Level | When |
|---|---|
| INFO | Normal operation — stage started, completed, row counts |
| WARNING | Unexpected but recoverable — null values filled |
| ERROR | Stage failed — exception message included |
| CRITICAL | Pipeline cannot continue |

---

## Data Schema

### hourly_weather_data

| Column | Type | Description |
|---|---|---|
| time | TIMESTAMP UNIQUE | Hour of forecast |
| temperature | DECIMAL | Temperature in °C |
| windspeed | DECIMAL | Windspeed in km/h |
| weathercode | INTEGER | WMO weather interpretation code |
| processed_at | TIMESTAMP | Pipeline execution timestamp |

```sql
CREATE TABLE hourly_weather_data (
    time         TIMESTAMP UNIQUE,
    temperature  DECIMAL,
    windspeed    DECIMAL,
    weathercode  INTEGER,
    processed_at TIMESTAMP
);
```

---

## Future Improvements

- Add retry logic with exponential backoff on extraction failure
- Schedule with Apache Airflow for automated runs
- Extend to multiple cities
- Add precipitation and humidity data
- Deploy to cloud (AWS/GCP)
- Add data quality checks with Great Expectations

---

## Author

Built as a data engineering learning project — Kaunas, Lithuania.
