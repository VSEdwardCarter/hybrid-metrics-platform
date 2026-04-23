# Hybrid Metrics Platform - Architecture

> For a high-level overview, see the main [README](../README.md)

---

## 📌 Purpose

This document describes the system architecture of the Hybrid Metrics Platform, including component responsibilities, data flow, and deployment considerations.

The platform is designed to demonstrate a **hybrid data engineering pattern** where:
- Data processing remains on-premises
- Metrics are derived and materialized locally
- Insights are exposed via an API for external consumption

---

## 🧠 Architectural Principles

### 1. Decoupled Compute and Serving
- Data processing is separated from data serving
- Metrics are precomputed and stored as artifacts
- API layer performs no heavy computation

---

### 2. API-First Design
- All external access occurs through a controlled service layer
- Raw data (Kafka, landing zone) is never exposed directly

---

### 3. Data Locality
- All ingestion and transformation occurs on-premises
- Only derived insights are shared externally

---

### 4. Observability as a First-Class Concern
- Metrics are treated as core outputs, not byproducts
- Pipeline health is explicitly modeled and exposed

---

## 🏗️ High-Level Architecture
```text
                ┌──────────────────────────┐
                │       Cloud UI           │
                │   (Next.js / Amplify)    │
                └────────────┬─────────────┘
                             │ HTTPS
                             ▼
                ┌──────────────────────────┐
                │       FastAPI Layer      │
                │   Metrics Endpoints      │
                └────────────┬─────────────┘
                             │ File Access
         ┌───────────────────┴───────────────────┐
         │                                       │
         ▼                                       ▼
┌────────────────────┐               ┌────────────────────┐
│   Metrics Storage   │               │   Processing Layer  │
│ (JSON Artifacts)    │               │   (PySpark / Batch) │
└─────────┬──────────┘               └─────────┬──────────┘
│                                    │
▼                                    ▼
┌───────────────┐                  ┌──────────────────┐
│  Landing Zone  │◄───────────────│      Kafka        │
│   (JSONL)      │                │   Event Stream    │
└───────────────┘                └──────────────────┘
```
---

## 🔧 Component Breakdown

### 1. Kafka (Streaming Layer)

**Role:**
- Event ingestion backbone

**Responsibilities:**
- Receive event payloads from producers
- Provide durable, ordered message streams

**Key Characteristics:**
- Topic: `signals`
- Partitioned for scalability (configurable)
- Acts as system entry point

---

### 2. Landing Zone (Bronze Layer)

**Role:**
- Immutable raw data storage

**Responsibilities:**
- Persist Kafka events to disk
- Maintain append-only structure
- Partition data by time

**Structure:**
landing/<topic>/dt=YYYY-MM-DD/hr=HH/*.jsonl

**Design Rationale:**
- Enables replayability
- Supports auditability
- Decouples ingestion from processing

---

### 3. Processing Layer (Silver → Gold)

**Role:**
- Transform and aggregate data into metrics

**Components:**
- PySpark jobs (or Python batch scripts)

**Responsibilities:**
- Normalize incoming data
- Apply data quality rules
- Detect late-arriving records
- Aggregate metrics

**Outputs:**
- Structured metric datasets

---

### 4. Metrics Storage (Gold Layer)

**Role:**
- Serve as the system’s query layer

**Structure:**
```
data/metrics/
├── total/
├── current/
└── baseline/
```
**Responsibilities:**
- Store precomputed metrics
- Provide fast read access for API
- Separate historical vs operational views

**Design Rationale:**
- Eliminates runtime aggregation
- Enables deterministic API responses
- Supports caching and scalability

---

### 5. FastAPI Service Layer

**Role:**
- Controlled access to system outputs

**Responsibilities:**
- Load metric artifacts from disk
- Expose REST endpoints
- Enforce response structure

**Endpoints:**
- /metrics/*
- /metrics/current/*

**Design Rationale:**
- Decouples frontend from backend logic
- Provides stable interface for consumers
- Aligns with enterprise API patterns

---

### 6. Frontend (Next.js)

**Role:**
- Visualization and user interaction

**Responsibilities:**
- Fetch metrics from API
- Display pipeline health indicators
- Provide operational insights

**Deployment Target:**
- AWS Amplify (cloud-hosted)

---

## 🔄 End-to-End Data Flow

1. Producers emit events → Kafka (`signals` topic)
2. Consumer writes events to landing zone (JSONL files)
3. Processing jobs read landing data
4. Metrics are computed and aggregated
5. Results written to metrics storage (JSON files)
6. FastAPI serves metrics via REST endpoints
7. Frontend consumes API and renders UI

---

## 🔐 Security & Access Considerations

- Kafka is not externally exposed
- Landing zone is internal-only
- API acts as the single access boundary
- Only aggregated, non-sensitive metrics are exposed

---

## ⚙️ Deployment Model

### On-Prem Components
- Kafka
- Landing Zone Storage
- Processing Jobs
- FastAPI Service

### Cloud Components
- Next.js UI (AWS Amplify)

---

## ⚖️ Tradeoffs

### Benefits
- Strong separation of concerns
- High performance API responses
- Controlled data exposure
- Alignment with regulated environments

### Limitations
- Metrics are batch-based (not real-time)
- JSON storage may not scale indefinitely
- Schema evolution is not yet formalized

---

## 🚧 Future Enhancements

- Streaming metrics (Kafka Streams / Spark Structured Streaming)
- Schema registry and contracts
- Metrics versioning
- Time-windowed aggregations
- Alerting and monitoring integration

---

## 📎 Summary

The architecture demonstrates:
- A hybrid deployment pattern
- A medallion-based data pipeline
- Decoupled ingestion, processing, and serving layers
- Metrics as a first-class data product