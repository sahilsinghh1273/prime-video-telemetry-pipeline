# Prime Video Telemetry Data Lake & Analytics Pipeline

## Project Overview
An end-to-end data engineering pipeline that simulates, ingests, transforms, and visualizes real-time streaming telemetry for a digital media platform. This project demonstrates core data engineering lifecycle skills including mock data generation, ETL processing, relational data warehousing, and business intelligence reporting.

## Architecture
1. **Data Generation & Ingestion (`generator.py`)**: An object-oriented Python script simulating continuous user clickstream and QoS (Quality of Service) telemetry (e.g., PLAY, PAUSE, BUFFERING, bitrate drops).
2. **Raw Storage (Data Lake)**: Raw JSON lines are appended to a local storage directory (`Local_Data_Lake/`) simulating an Amazon S3 landing zone.
3. **ETL Processing (`etl_processor.py`)**: A Python processor that extracts the raw logs, cleans malformed text, applies business logic to identify buffering anomalies, and loads the structured output into a relational database.
4. **Data Warehouse (SQLite)**: A relational database schema (`prime_video_warehouse.db`) designed to aggregate metrics for fast analytical querying.
5. **Business Intelligence (`dashboard.py`)**: A Matplotlib visualization layer querying the data warehouse to generate a QoS dashboard for engineering managers.

## Downstream ML Integration
The transformed telemetry dataset is structured for export to Google Drive storage directories to serve as reasoning and diagnostic data. This pipeline prepares the data for parameter-efficient fine-tuning (LoRA) of causal language models (e.g., Qwen2.5-0.5B-Instruct), bridging the gap between raw data ingestion and advanced machine learning workflows.

## How to Run
1. **Start the Live Data Stream**:
   ```bash
   python generator.py
   ```
2. **Process and Load the Data**:
   ```bash
   python etl_processor.py
   ```
3. **Launch the Analytics Visualization**:
   ```bash
   python dashboard.py
   ```
4. **Sync Data Lake to Cloudinary (Cloud Storage)**:
   ```bash
   python cloudinary_sync.py
   ```

## Cloud Deployment & Assets
The data lake artifacts are deployed to the cloud via Cloudinary:
- **Quality of Service (QoS) Dashboard**: [Live Chart Image](https://res.cloudinary.com/pqspfq9j/image/upload/v1795511686/prime_video_telemetry/buffering_report.png.png)
- **Raw Telemetry Logs**: [JSONL Stream](https://res.cloudinary.com/pqspfq9j/raw/upload/v1795511626/prime_video_telemetry/raw_streaming_logs.jsonl)
- **Analytical SQLite Warehouse**: [Warehouse DB](https://res.cloudinary.com/pqspfq9j/raw/upload/v1795511625/prime_video_telemetry/prime_video_warehouse.db)

## AWS Cloud Migration Path
To scale this local architecture to an enterprise-grade cloud deployment on AWS:
- **Telemetry Ingestion**: Migrate `generator.py` to an AWS Lambda function or Amazon Kinesis Data Streams.
- **Landing Zone**: Change the storage destination from `Local_Data_Lake` to an Amazon S3 bucket.
- **Distributed ETL Processing**: Migrate `etl_processor.py` logic into AWS Glue (PySpark) or AWS EMR.
- **Cloud Data Warehouse**: Replace SQLite with Amazon Athena (serverless querying over S3) or Amazon Redshift.
- **Enterprise BI**: Rebuild the `dashboard.py` chart using Amazon QuickSight dashboards.

