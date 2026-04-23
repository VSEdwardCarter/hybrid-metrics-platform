# 🚀 Hybrid Metrics Platform
# A Hybrid Data Engineering Platform for Operational Observability

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![PySpark](https://img.shields.io/badge/PySpark-Data%20Processing-orange)
![Kafka](https://img.shields.io/badge/Kafka-Streaming-black)
![Next.js](https://img.shields.io/badge/Next.js-Frontend-lightgrey)
![AWS Amplify](https://img.shields.io/badge/AWS-Amplify-ff9900)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid-blueviolet)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

---

## 📌 Overview

The Hybrid Metrics Platform is a production-style data engineering system designed to demonstrate how modern data platforms operate under real-world enterprise constraints.

This project simulates a hybrid architecture where:
- Data processing remains on-premises
- User interfaces are cloud-hosted
- Operational insights are exposed through curated APIs

Rather than exposing raw data streams, the platform delivers precomputed, decision-ready metrics that reflect pipeline health, performance, and data quality.

---

## 🎯 Problem Statement

In regulated and enterprise environments (e.g., government, defense, financial systems):

- Data cannot always leave controlled environments
- Systems must still provide real-time operational visibility
- Teams require trustworthy, explainable metrics—not raw data

This platform addresses that gap by treating pipeline observability as a first-class data product.

---

## 🧠 Key Concepts

### 1. Metrics as a Data Product
Instead of querying raw pipelines, this system produces:
- Throughput metrics
- Late-arriving data percentages
- Data quality / quarantine rates

These are:
- Precomputed
- Versioned
- Served via API

---

### 2. Hybrid Architecture
- On-Prem Layer
  - Kafka (event streaming)
  - Landing Zone (JSONL persistence)
  - PySpark (medallion transformations)

- Service Layer
  - FastAPI exposing curated metrics

- Cloud Layer
  - Next.js UI (designed for AWS Amplify deployment)

---

### 3. Medallion Data Model
The pipeline follows a structured progression:

- Bronze → Raw ingestion (Kafka → JSONL)
- Silver → Validated, structured data
- Gold → Aggregated metrics and observability outputs

Data quality enforcement occurs between layers, with invalid records routed to quarantine datasets for traceability.

---

## 🏗️ Architecture
```
                ┌──────────────────────────┐
                │       Cloud UI           │
                │   (Next.js / Amplify)    │
                └────────────┬─────────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │       FastAPI Layer      │
                │  /metrics/* endpoints    │
                └────────────┬─────────────┘
                             │
         ┌───────────────────┴───────────────────┐
         │                                       │
         ▼                                       ▼
┌────────────────────┐               ┌────────────────────┐
│   Metrics Store     │               │   PySpark Jobs      │
│ (JSON Snapshots)    │               │ (Medallion Logic)   │
└─────────┬──────────┘               └─────────┬──────────┘
│                                    │
▼                                    ▼
┌───────────────┐                  ┌──────────────────┐
│  Landing Zone  │◄───────────────│      Kafka        │
│   (JSONL)      │                │   Topic: signals  │
└───────────────┘                └──────────────────┘
```
---

## 📊 Metrics Exposed

Cumulative Metrics:
- /metrics/throughput
- /metrics/late-data
- /metrics/quarantine

Operational Snapshot Metrics:
- /metrics/current/throughput
- /metrics/current/late-data
- /metrics/current/quarantine

---

## ⚙️ Design Decisions

### Why Precomputed Metrics?
- Eliminates runtime query cost
- Ensures deterministic outputs
- Enables API-level SLAs
- Decouples compute from serving

### Why JSON-Based Metric Storage?
- Lightweight and portable
- Easy to version and cache
- Simplifies API integration
- Reflects real-world batch aggregation patterns

### Why Not Expose Kafka Directly?
- Reduces system coupling
- Improves security posture
- Aligns with enterprise API-first patterns

---

## 🧪 Data Pipeline

### Ingestion
Kafka producers emit event data (signals topic)

Consumer writes append-only JSONL files:
/landing/<topic>/dt=YYYY-MM-DD/hr=HH/*.jsonl

### Processing
PySpark jobs:
- Normalize schema
- Apply data quality rules
- Route invalid records to quarantine

### Aggregation
Metrics derived from processed datasets:
- Throughput counts
- Late-arrival detection
- Data quality violations

---

## 🔍 Observability Focus

- Pipeline health tracking
- Data quality enforcement
- Latency awareness (late data)
- Transparent failure handling (quarantine)

---

## 🚧 Roadmap

- Streaming metrics (Kafka Streams / Spark Structured Streaming)
- Time-windowed trend analysis
- Impact modeling for late-arriving data
- Schema contracts and versioning
- Cloud deployment via AWS Amplify

---

## 📚 Documentation

- docs/overview.md
- docs/architecture.md
- docs/pipeline.md
- docs/api.md

---

## 🧑‍💻 Summary

The Hybrid Metrics Platform demonstrates how to:

- Build a decoupled, observable data pipeline
- Deliver actionable metrics instead of raw data
- Operate across hybrid infrastructure boundaries