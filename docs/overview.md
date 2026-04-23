# Hybrid Metrics Platform - Technical Overview

## 📌 Purpose

This document provides a technical overview of the Hybrid Metrics Platform, including system components, data flow, and implementation details.

The platform simulates a hybrid data engineering architecture where:
- Data ingestion and processing occur on-premises
- Metrics are derived from pipeline outputs
- A service layer exposes curated metrics for external consumption

---

## 🧱 Repository Structure
```text
hybrid-metrics/
├── hybrid-metrics-api/
│   └── app/
│       ├── main.py
│       ├── api/routes/
│       ├── services/
│       ├── models/
│       └── core/
├── hybrid-metrics-ui/
│   └── src/
│       ├── app/
│       ├── components/
│       └── lib/
├── data/
│   └── metrics/
│       ├── total/
│       ├── current/
│       └── baseline/
└── scripts/
├── initial_load_metrics.py
├── incremental_load_metrics.py
└── metrics_common.py
```
---

## ⚙️ System Components

### 1. Kafka (Ingestion Layer)
- Topic: `signals`
- Acts as the event streaming backbone
- Producers emit structured event payloads

---

### 2. Landing Zone (Raw Storage)
- Append-only JSONL files
- Partitioned by:
  - Date (dt=YYYY-MM-DD)
  - Hour (hr=HH)

Example:
landing/<topic>/dt=2026-03-01/hr=10/signals-20260301-10.jsonl

- Stores raw, immutable data
- Serves as the Bronze layer

---

### 3. Metrics Processing (Batch Layer)

Scripts:
- `initial_load_metrics.py`
- `incremental_load_metrics.py`

Responsibilities:
- Read landing zone JSONL data
- Aggregate pipeline metrics
- Detect:
  - Throughput
  - Late-arriving data
  - Data quality issues

---

### 4. Metrics Storage

Generated outputs stored as JSON:
```text
data/metrics/
├── total/       # cumulative metrics
├── current/     # current operational snapshot
└── baseline/    # reference metrics
```
Design Notes:
- Files are gitignored
- Treated as derived artifacts
- Enable fast API responses

---

### 5. FastAPI Service Layer

Entry point:
app/main.py

Endpoints:
- /metrics/throughput
- /metrics/late-data
- /metrics/quarantine

Current state endpoints:
- /metrics/current/throughput
- /metrics/current/late-data
- /metrics/current/quarantine

Responsibilities:
- Read precomputed metric JSON files
- Serve structured responses
- Decouple frontend from raw data pipeline

Run locally:
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

---

### 6. Frontend (Next.js)

Location:
hybrid-metrics-ui/

Responsibilities:
- Fetch metrics via API
- Display pipeline health indicators
- Provide operational visibility

Key files:
- components/MetricCard.tsx
- lib/api.ts

---

## 🔄 Data Flow

1. Kafka producers emit events → `signals` topic
2. Consumer writes events to landing zone (JSONL)
3. Metrics scripts process landing data
4. Aggregated metrics written to JSON files
5. FastAPI serves metrics via REST endpoints
6. UI consumes API and displays results

---

## 📊 Metrics Definitions

### Throughput
- Count of records processed over time

### Late Data
- Percentage of records arriving outside expected time window

### Quarantine
- Count of records failing data quality rules

---

## 🧪 Execution Workflow

### Initial Load
Used for full dataset processing:
python scripts/initial_load_metrics.py

### Incremental Load
Used for ongoing updates:
python scripts/incremental_load_metrics.py

---

## ⚠️ Assumptions & Constraints

- Metrics are batch-derived (not streaming)
- JSON files act as a serving layer
- Kafka is not directly exposed externally
- Data quality rules are embedded in processing scripts

---

## 🚧 Known Gaps / Future Improvements

- Streaming aggregation (Kafka Streams / Spark)
- Schema validation and contracts
- Metrics versioning
- Time-windowed analytics
- Alerting / monitoring integration

---

## 📎 Summary

This implementation demonstrates:
- A medallion-style data pipeline
- Decoupled compute and serving layers
- Metrics-first data product design
- Hybrid architecture pattern (on-prem data, cloud UI)