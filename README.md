# Weather ETL Pipeline

A modular, production-inspired data engineering pipeline that automates the extraction, transformation, and storage of real-time weather data for Kaunas, Lithuania.

---

## Overview

This project demonstrates a professional ETL architecture built with Python and PostgreSQL. Weather metrics are fetched from the Open-Meteo API, cleaned and normalized with Pandas, and persisted into a containerized PostgreSQL database — with full logging and error handling at every stage.

---

## Features

- **Extract** — Stateless GET requests to the Open-Meteo API, retrieving nested JSON weather metrics with retry-safe error handling
- **Transform** — JSON-to-DataFrame conversion, UTC datetime normalization, and `processed_at` metadata injection for auditability
- **Load** — Append strategy to PostgreSQL via SQLAlchemy, maintaining full historical records on every run
- **Logging** — Simultaneous console and file logging with structured format across all pipeline stages
- **Error Handling** — Per-stage exception handling with descriptive error messages and graceful failure
- **Containerized Database** — PostgreSQL 15 running in Docker with persistent volume storage
- **Secure Configuration** — Decoupled credentials via `.env` files, never committed to version control

---

## Tech Stack

| Category | Tool |
|---|---|
| Language | Python 3.x |
| Data Processing | Pandas |
| HTTP Client | Requests |
| ORM | SQLAlchemy |
| Database Driver | Psycopg2 |
| Database | PostgreSQL 15 |
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
│   ├── transform.py      # Data cleaning and normalization
│   ├── load.py           # Database connection and persistence
│   └── logger.py         # Centralized logging configuration
├── logs/
│   └── pipeline.log      # Pipeline execution logs
├── .env                  # Local credentials (not committed)
├── .env.example          # Credential template for new contributors
├── .gitignore
├── docker-compose.yml    # PostgreSQL service definition
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

Execute the full pipeline:

```bash
python main.py
```

### Expected log output

```
2026-05-09 09:15:03 | INFO     | main       | Pipeline started
2026-05-09 09:15:03 | INFO     | main       | Starting extraction
2026-05-09 09:15:03 | INFO     | extract    | Extraction started
2026-05-09 09:15:04 | INFO     | extract    | Extraction successful
2026-05-09 09:15:04 | INFO     | main       | Extraction complete
2026-05-09 09:15:04 | INFO     | main       | Starting transformation
2026-05-09 09:15:04 | INFO     | transform  | Transformation started
2026-05-09 09:15:04 | INFO     | transform  | Converting datetime
2026-05-09 09:15:04 | INFO     | transform  | Transformation complete
2026-05-09 09:15:04 | INFO     | main       | Starting load
2026-05-09 09:15:04 | INFO     | load       | Load successful
2026-05-09 09:15:04 | INFO     | main       | Pipeline complete
```

### Verify data in database

```bash
docker exec -it weather_postgres psql -U myuser -d weather_db -c "SELECT * FROM weather_data;"
```

---

## Reliability & Observability

### Error Handling

| Stage | Failure Scenario | Behaviour |
|---|---|---|
| Extract | API unreachable | Logs error, raises exception, pipeline stops |
| Extract | Bad HTTP response (4xx/5xx) | Logs status code, raises exception |
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

## Future Improvements

- Add retry logic with exponential backoff on extraction failure
- Implement UPSERT to prevent duplicate weather readings
- Schedule with Apache Airflow for automated runs
- Add data quality validation before load
- Extend to multiple cities
- Add Grafana dashboard for live monitoring

---

## Data Schema

```sql
CREATE TABLE weather_data (
    time            TIMESTAMP,
    interval        INTEGER,
    temperature     DECIMAL,
    windspeed       DECIMAL,
    winddirection   INTEGER,
    is_day          INTEGER,
    weathercode     INTEGER,
    processed_at    TIMESTAMP
);
```

---

## Author

Built as a data engineering learning project — Kaunas, Lithuania.
