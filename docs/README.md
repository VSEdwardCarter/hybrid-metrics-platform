# Hybrid Metrics Platform

Hybrid data platform demonstrating an end-to-end flow from on-prem streaming pipelines to a cloud-ready dashboard.

## Overview

This project simulates a real-world hybrid architecture where:

- Streaming data is generated and processed on-prem (Kafka + Python pipelines)
- Metrics are derived from pipeline outputs and exposed via a FastAPI service
- A frontend dashboard (Next.js) consumes these metrics for visualization

The system separates **cumulative (total)** metrics from **current operational snapshots**, enabling both historical context and real-time insights.

---

## Architecture
```text
[Kafka (on-prem)]
  ↓
  Landing Zone (JSONL)
  ↓
  Metrics Generation (Python)
  ├── total (cumulative view)
  └── current (latest partition)
  ↓
  FastAPI Service
  ↓
  Next.js Dashboard (UI)

```

## Repository Structure
```text
hybrid-metrics/
├── hybrid-metrics-api/ # FastAPI backend + metrics processing
└── hybrid-metrics-ui/ # Next.js dashboard (in progress)
```


---

## Key Concepts

- **Hybrid Architecture**: Data remains on-prem while UI is cloud-ready
- **Decoupled Layers**: Pipelines, metrics, API, and UI are independent
- **Total vs Current Metrics**:
    - `total` → cumulative system state
    - `current` → latest operational snapshot
- **Incremental Processing**: Metrics can be refreshed without reprocessing all data

---

## API Highlights

### Total Metrics
- `/metrics/throughput`
- `/metrics/late-data`
- `/metrics/quarantine`

### Current Metrics
- `/metrics/current/throughput`
- `/metrics/current/late-data`
- `/metrics/current/quarantine`

---

## Status

- Backend (FastAPI + metrics pipeline): ✅ Implemented
- Incremental metrics processing: ✅ Implemented
- Frontend dashboard (Next.js): 🚧 In progress

---

## Next Steps

- Build UI dashboard
- Add scheduling for incremental refresh
- Extend metrics (time-series, trends)
- Deploy UI to cloud (AWS Amplify)