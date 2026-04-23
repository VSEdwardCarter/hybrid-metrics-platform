# Hybrid Metrics Platform - Data Pipeline

> For system architecture, see [architecture.md](architecture.md)

---

## 📌 Purpose

This document describes the data pipeline implementation of the Hybrid Metrics Platform, including ingestion, transformation, and metric generation.

The pipeline follows a **medallion architecture (Bronze → Silver → Gold)** and is designed to:
- Preserve raw data fidelity
- Enforce data quality
- Produce reliable, explainable metrics

---

## 🧠 Pipeline Principles

### 1. Immutable Raw Data
- All incoming data is stored without modification
- Enables replay and auditability

---

### 2. Progressive Refinement
- Data is incrementally improved across layers
- Each layer has a defined responsibility

---

### 3. Separation of Concerns
- Ingestion, validation, and aggregation are independent steps
- Failures are isolated and traceable

---

### 4. Observability-Driven Design
- Metrics are derived directly from pipeline behavior
- Pipeline health is measurable and exposed

---

## 🏗️ Pipeline Overview

Kafka → Landing Zone (Bronze) → Processing (Silver) → Aggregation (Gold) → Metrics API

---

## 🥉 Bronze Layer - Ingestion

### Source
- Kafka topic: `signals`

### Consumer Behavior
- Reads messages from Kafka
- Writes records to append-only JSONL files

### Storage Pattern

landing/<topic>/dt=YYYY-MM-DD/hr=HH/<topic>-YYYYMMDD-HH.jsonl

### Record Structure
Each record typically contains:
- Event payload
- Timestamp (`ts` if present)
- Kafka metadata (fallback timestamp if needed)

### Key Characteristics
- Append-only
- Time-partitioned
- No transformation applied

---

## 🥈 Silver Layer - Validation & Normalization

### Purpose
- Transform raw JSON into structured format
- Apply data quality rules
- Prepare data for aggregation

---

### Transformation Strategy

The pipeline supports **type-aware parsing**:

- Each record includes a `type` field
- Parsing logic is applied based on `type`
- Fields are normalized into a consistent schema

Example:
```json
Raw:
{
"type": "A",
"content": { ... }
}

Silver:
{
"created_date": "...",
"applicability_time": "...",
"type": "A",
"field_1": value,
"field_2": value,
...
"raw_json": {...}
}
```
---

### Design Decision: Universal Raw Column

A final column preserves the original payload:

- `raw_json` (or equivalent)
- Ensures no data loss
- Allows Gold layer to fallback if needed

---

### Data Quality Rules

Examples:
- Required timestamps present
- Valid numeric ranges
- Schema consistency checks

---

### Outcomes

Each record is classified as:

- **Valid** → Passed to aggregation
- **Invalid** → Sent to quarantine dataset

---

## 🚨 Quarantine Handling

### Purpose
- Preserve invalid records
- Enable investigation and traceability

### Storage
- Separate dataset from valid records

### Example Reasons
- Missing required fields
- Invalid timestamps
- Out-of-range values

---

## 🥇 Gold Layer - Metrics Aggregation

### Purpose
- Produce aggregated metrics from processed data

---

### Metrics Computed

#### 1. Throughput
- Count of processed records over time

#### 2. Late Data
- Records arriving outside expected time window

Detection:
- Compare event timestamp vs ingestion time

#### 3. Quarantine Rate
- Percentage or count of invalid records

---

### Aggregation Strategy

- Batch processing
- Derived from Silver layer outputs
- Stored as JSON artifacts

---

## 📂 Metrics Output Structure
```
data/metrics/
├── total/
├── current/
└── baseline/
```
---

### total/
- Full historical aggregation

### current/
- Recent operational snapshot

### baseline/
- Reference dataset for comparison

---

## 🔄 Execution Modes

### Initial Load

Purpose:
- Process full dataset

Command:
```python python scripts/initial_load_metrics.py```

---

### Incremental Load

Purpose:
- Process new data only

Command:
```python python scripts/incremental_load_metrics.py```

---

## ⏱️ Late Data Handling

### Definition
Data is considered "late" if:
- Event timestamp is outside expected processing window

---

### Current Approach
- Rule-based detection
- Counted as part of metrics

---

### Future Direction
- Weighted impact scoring
- Statistical detection (e.g., IQR-based thresholds)
- ML-driven decisioning

---

## 📊 Data Flow Summary

1. Kafka emits events
2. Consumer writes JSONL to landing zone
3. Processing layer reads and validates data
4. Invalid records → quarantine
5. Valid records → aggregation
6. Metrics written to JSON
7. API serves results

---

## ⚠️ Constraints

- Batch-based processing (not streaming)
- Schema evolution is implicit
- Data quality rules are embedded in code

---

## 🚧 Future Enhancements

- Streaming pipeline (Spark Structured Streaming / Kafka Streams)
- Formal schema contracts
- Centralized DQ rule engine
- Metrics versioning
- Partition pruning optimization

---

## 📎 Summary

The pipeline demonstrates:

- Medallion architecture implementation
- Data quality enforcement with quarantine handling
- Late data detection and measurement
- Metrics generation as a downstream data product