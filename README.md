# Reddit Stream Processing with Kafka, Spark, and PostgreSQL

Real-time post stream on Reddit, which has become a crash course in Apache tools.

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Kafka Producer](#kafka-producer)
- [Spark Consumer](#spark-consumer)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

---

## Project Overview

This project processes real-time Reddit comments using Kafka, Spark, and PostgreSQL. The pipeline consists of:

1. **Kafka Producer**: Fetches new Reddit comments and sends them to a Kafka topic.
2. **Kafka Broker**: Handles the event stream.
3. **Spark Consumer**: Consumes Kafka messages, processes them, and writes them to a PostgreSQL database.
4. **PostgreSQL**: Stores the structured data for further analysis.

## Architecture

```
Reddit -> Kafka Producer -> Kafka Broker -> Spark Consumer -> PostgreSQL
```

Each component runs in a separate Docker container, orchestrated using `docker-compose`.

## Technologies Used

- **Python** (Kafka Producer, Spark Consumer)
- **Apache Kafka** (Streaming Platform)
- **Apache Spark** (Stream Processing)
- **PostgreSQL** (Database Storage)
- **Docker & Docker Compose** (Containerization)
- **uv** (modern Python package manager)

## Prerequisites

Ensure you have the following installed:

- **Docker** and **Docker Compose**
- **Python 3.12** (for local testing)
- **Reddit API credentials** (for Kafka producer)
- **uv** (optional, for Python package management)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reddit-streaming-pipeline.git
cd reddit-streaming-pipeline
```
2. Create a `.env` file with the required environment variables.
3. Install Python dependencies locally (optionally):
```bash
uv sync
```

## Environment Variables

Create a `.env` file in the root directory as it is described in the `.env.example` file.

## Running the Project

1. Start all services using Docker Compose:
```bash
docker-compose up -d
```

2. Verify that all containers are running:
```bash
docker ps
```

## Kafka Producer

The **Kafka Producer** fetches comments from Reddit and pushes them to the Kafka topic.

### Running Producer Manually

To run the producer locally (if needed):

```bash
python producer/kafka_producer.py
```

## Spark Consumer

The **Spark Consumer** reads messages from Kafka, processes them, and writes to PostgreSQL.

### Running Spark Consumer Manually

To run the consumer locally (if needed):

```bash
spark-submit --master local[2] consumer/spark_consumer.py
```

## PostgreSQL Database

The schema of the database is stored in the `db_init/` directory and automatically applied when the PostgreSQL container starts.

To verify that data is being correctly inserted into the PostgreSQL database, you can connect to the PostgreSQL container:
```bash
docker exec -it postgres psql jdbc:postgresql://postgres:5432/reddit_db -U your_user
```
and run a query to check the inserted records:
```sql
SELECT * FROM reddit_msgs LIMIT 10;
```

## Troubleshooting

- **Kafka broker not available?** Ensure Kafka and Zookeeper are running:
```bash
docker logs zookeeper
docker logs kafka_broker
```
- **Messages not appearing in PostgreSQL?** Check Spark logs:
```bash
docker logs spark_consumer
```
- **Verify messages in Kafka topic:**
```bash
docker exec -it kafka_producer kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic reddit_comments_stream --from-beginning
```

## Future Improvements

- Implement monitoring using **Prometheus** and **Grafana**
- Deploy using **Kubernetes**
- Introduce real-time dashboards using **Apache Superset**

