# Hybrid Metrics API

FastAPI service for exposing aggregated on-prem pipeline metrics to a cloud-hosted dashboard.

## Endpoints

- `GET /health`
- `GET /metrics/throughput`
- `GET /metrics/late-data`
- `GET /metrics/quarantine`

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
# Hybrid Metrics API

A production-style FastAPI service that exposes **aggregated data pipeline metrics** from an on-prem environment to a cloud-hosted dashboard.

---

## 🧭 Overview

This project simulates a **real-world hybrid data architecture**:

* **On-Prem (Lab Environment)**

  * Kafka (k3s single-node cluster)
  * PySpark pipelines (medallion architecture)
  * Landing zone (JSONL signal ingestion)
  * Aggregated pipeline metrics (JSON snapshots)

* **Cloud (Planned)**

  * Next.js dashboard (AWS Amplify)
  * CI/CD via GitHub

* **API Layer (This Project)**

  * FastAPI service running locally
  * Exposes **curated metrics only** (not raw streaming data)

---


## 🧱 Architecture

```text
[On-Prem Lab]

Kafka (k3s NodePort)
    ↓
Landing Consumer (JSONL files)
    ↓
Metric Aggregation (JSON snapshots)
    ↓
FastAPI (this service)
    ↓
[Future]
Next.js Dashboard (AWS)
```

---

## 🎯 Purpose

This API provides a clean abstraction layer between:

* **Operational data pipelines (on-prem)**
* **User-facing dashboards (cloud)**

It enforces a key architectural principle:

> Do not expose raw streaming data — expose curated, aggregated metrics.

---

## 📂 Project Structure

```text
hybrid-metrics-api/
├── app/
│   ├── main.py
│   ├── core/
│   │   └── config.py
│   ├── api/
│   │   └── routes/
│   │       └── metrics.py
│   ├── models/
│   │   └── metrics.py
│   └── services/
│       └── metrics_service.py
├── data/
│   └── metrics/
│       ├── throughput.json
│       ├── late_data.json
│       └── quarantine.json
├── requirements.txt
└── README.md
```

---

## 🔌 API Endpoints

### Health

```http
GET /health
```

---

### Throughput Metrics

```http
GET /metrics/throughput
```

Returns:

* records processed
* processing window
* records per minute

---

### Late Data Metrics

```http
GET /metrics/late-data
```

Returns:

* late record counts
* percentage of late arrivals
* measurement window

---

### Quarantine Metrics

```http
GET /metrics/quarantine
```

Returns:

* quarantined record counts
* reason breakdown (data quality failures)

---

## 📊 Data Source (Current)

Metrics are currently read from local JSON files:

```text
data/metrics/
```

These files simulate outputs from pipeline processing layers and are structured to be easily replaced with:

* PySpark outputs
* Parquet datasets
* Postgres tables
* or streaming aggregations

---

## ⚙️ Running Locally

### 1. Create environment

```bash
python3 -m venv hybrid-metrics
source hybrid-metrics/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

### 4. Open docs

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Example Response

```json
{
  "data": [
    {
      "pipeline_name": "signals_gold_pipeline",
      "records_processed": 42000,
      "window_start": "2026-03-21T21:00:00Z",
      "window_end": "2026-03-21T22:00:00Z",
      "records_per_minute": 700.0
    }
  ]
}
```

---

## 🔄 Design Principles

### 1. Separation of Concerns

* **Routes** → HTTP layer
* **Services** → data retrieval logic
* **Models** → response contracts

---

### 2. Replaceable Data Sources

The service layer allows swapping:

```text
JSON → Parquet → Database → Streaming Aggregates
```

without changing API endpoints.

---

### 3. Hybrid-Ready

* Data stays **on-prem**
* UI lives **in the cloud**
* API acts as a **secure boundary**

---

## 🚀 Roadmap

### Phase 1 (Current)

* FastAPI service with JSON-backed metrics
* Local dev environment
* Modular architecture

### Phase 2

* Integrate PySpark pipeline outputs
* Automate metric generation
* Add timestamped snapshots

### Phase 3

* Add authentication (API keys / JWT)
* Introduce caching layer (Redis)
* Add rate limiting

### Phase 4

* Deploy Next.js dashboard (AWS Amplify)
* Connect frontend to API
* Implement CI/CD pipeline

---

## 🧠 Why This Project Matters

This project demonstrates:

* Hybrid cloud architecture design
* Real-time + batch pipeline integration
* API abstraction over streaming systems
* Production-style Python service design
* Kubernetes + Kafka operational awareness

---

## 📌 Notes

* Designed to run alongside a local k3s-based Kafka cluster
* Uses NodePort exposure for Kafka access
* Optimized for low-resource lab environments

---

## 👤 Author

Edward Carter
Senior Data Engineer
