Weather ETL Pipeline

A modular Data Engineering pipeline that automates the collection, cleaning, and storage of weather data for Kaunas, Lithuania. This project demonstrates a professional ETL (Extract, Transform, Load) architecture using Python and PostgreSQL.
🚀 Features

    Extract: Fetches real-time weather metrics from the Open-Meteo API.

    Transform: Cleans nested JSON, handles datetime conversions, and adds processing metadata using Pandas.

    Load: Persists data into a PostgreSQL database using SQLAlchemy.

    Infrastructure: Fully containerized database using Docker Compose.

    Environment Management: Secure configuration using .env files to protect credentials.

🛠 Tech Stack

    Language: Python 3.x

    Libraries: Pandas, Requests, SQLAlchemy, Psycopg2, Python-dotenv

    Database: PostgreSQL 15

    DevOps: Docker, Docker Compose

    Version Control: Git

⚙️ Setup & Installation
1. Clone the repository
Bash

git clone <your-repo-url>
cd weather-etl-project

2. Configure Environment Variables

Create a file named .env in the root directory and add the following:
Ini, TOML

DB_USER=myuser
DB_PASSWORD=mypassword
DB_HOST=localhost
DB_PORT=5232
DB_NAME=weather_db

3. Launch the Database

Start the PostgreSQL container in detached mode:
Bash

docker compose up -d

4. Install Python Dependencies

Ensure you have your virtual environment activated:
Bash

pip install -r requirements.txt

🏃 How to Run

To execute the full pipeline from start to finish, run the orchestrator script:
Bash

python main.py

Verifying the Data

To confirm the data has been successfully loaded into the database, query the table directly via Docker:
Bash

docker exec -it weather_postgres psql -U myuser -d weather_db -c "SELECT * FROM weather_data;"

📂 Project Structure

    extract.py: Logic for connecting to the Open-Meteo API and retrieving raw JSON.

    transform.py: Data cleaning, renaming columns, and adding timestamps via Pandas.

    load.py: Database connection logic using SQLAlchemy engines.

    main.py: The "Orchestrator" script that runs the E, T, and L functions in sequence.

    docker-compose.yml: Defines the PostgreSQL service and persistent data volumes.

    requirements.txt: List of necessary Python packages.