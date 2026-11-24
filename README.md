# Prime Video Telemetry Data Lake & Analytics Pipeline

## Project Overview
An end-to-end data engineering pipeline that simulates, ingests, transforms, visualizes, and cloud-deploys real-time streaming telemetry for a digital media platform. This project demonstrates core data engineering lifecycle skills including mock telemetry generation, ETL processing, relational data warehousing, cloud data lake deployment, and executive business intelligence reporting.

---

## Visual QoS Dashboard (Cloud Deployed)
![Prime Video Quality of Service Dashboard](https://res.cloudinary.com/pqspfq9j/image/upload/v1795511686/prime_video_telemetry/buffering_report.png.png)

---

## Architecture
1. **Data Generation & Ingestion (`generator.py`)**: An object-oriented Python engine simulating continuous user clickstream and QoS (Quality of Service) telemetry (e.g., `PLAY`, `PAUSE`, `BUFFERING`, bitrate adjustments).
2. **Local Landing Zone (`Local_Data_Lake/`)**: Partitioned raw JSON lines and custom streaming logs appended in real-time.
3. **Cloud Data Lake Storage (`Cloudinary` & `cloudinary_sync.py`)**: All raw telemetry logs, database artifacts, and visual reports are continuously synchronized and hosted in the cloud on Cloudinary.
4. **ETL Processing (`etl_processor.py`)**: A Python pipeline that extracts raw streaming logs, cleans malformed text, applies business logic to detect buffering anomalies, and loads structured metrics into a relational warehouse.
5. **Data Warehouse (SQLite)**: A relational schema (`prime_video_warehouse.db`) designed to aggregate metrics for fast analytical SQL querying.
6. **Business Intelligence (`dashboard.py`)**: A visualization layer querying the data warehouse to generate executive QoS reports for engineering managers.

---

## Live Cloud Deployment & Assets
All pipeline artifacts are deployed live on **Cloudinary**:
- 📊 **QoS Analytics Dashboard**: [View Hosted Chart Image](https://res.cloudinary.com/pqspfq9j/image/upload/v1795511686/prime_video_telemetry/buffering_report.png.png)
- 📄 **Raw Telemetry Stream**: [View Raw JSONL Logs](https://res.cloudinary.com/pqspfq9j/raw/upload/v1795511626/prime_video_telemetry/raw_streaming_logs.jsonl)
- 🗄️ **Relational Warehouse DB**: [Download SQLite Warehouse](https://res.cloudinary.com/pqspfq9j/raw/upload/v1795511625/prime_video_telemetry/prime_video_warehouse.db)
- 📁 **Partitioned Event Logs**: [View Date Partition](https://res.cloudinary.com/pqspfq9j/raw/upload/v1795511627/prime_video_telemetry/streaming_events_2026-11-05.jsonl)

---

## Downstream ML Integration
The transformed telemetry dataset is structured for export to serve as reasoning and diagnostic data. This pipeline prepares the dataset for parameter-efficient fine-tuning (LoRA) of causal language models (e.g., Qwen2.5-0.5B-Instruct), bridging the gap between raw data ingestion and advanced machine learning workflows.

---

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

---

## AWS Cloud Migration Roadmap
To scale this architecture to an enterprise AWS deployment:
- **Telemetry Ingestion**: Migrate `generator.py` to an AWS Lambda function or Amazon Kinesis Data Streams.
- **Enterprise Landing Zone**: Map Cloudinary raw storage to an Amazon S3 bucket.
- **Distributed ETL Processing**: Scale `etl_processor.py` logic into AWS Glue (PySpark) or AWS EMR.
- **Cloud Data Warehouse**: Query S3 directly using Amazon Athena (serverless SQL) or load into Amazon Redshift.
- **Enterprise BI**: Rebuild the Matplotlib chart using Amazon QuickSight dashboards.
