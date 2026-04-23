# Hybrid Metrics Platform - API Reference

> For system architecture, see [architecture.md](architecture.md)  
> For pipeline details, see [pipeline.md](pipeline.md)

---

## 📌 Overview

The Hybrid Metrics Platform exposes a REST API for accessing precomputed pipeline metrics.

The API is designed to:
- Provide fast, deterministic responses
- Abstract underlying data processing complexity
- Serve as the single access point for external consumers

---

## 🌐 Base URL

Local:
http://127.0.0.1:8000

---

## ⚙️ API Characteristics

- Protocol: HTTP/REST
- Format: JSON
- Data Source: Precomputed metric artifacts (JSON files)
- Compute Model: No runtime aggregation

---

## 📊 Available Endpoints

### 1. Throughput Metrics

#### GET /metrics/throughput

**Description:**
Returns cumulative throughput metrics.

**Response Example:**
```json
{
"metric": "throughput",
"total_records": 125000,
"time_range": {
  "start": "2026-03-01T00:00:00Z",
  "end": "2026-03-31T23:59:59Z"
  }
}
```
---

### 2. Late Data Metrics

#### GET /metrics/late-data

**Description:**
Returns cumulative late-arriving data metrics.

**Response Example:**
```json
{
"metric": "late_data",
"late_records": 4200,
"late_percentage": 3.36
}
```
---

### 3. Quarantine Metrics

#### GET /metrics/quarantine

**Description:**
Returns cumulative data quality failure metrics.

**Response Example:**
```json
{
"metric": "quarantine",
"invalid_records": 3100,
"failure_reasons": {
  "missing_timestamp": 1200,
  "invalid_format": 900,
  "out_of_range": 1000
  }
}
```
---

## ⚡ Current State Endpoints

These endpoints provide a near real-time operational snapshot.

---

### GET /metrics/current/throughput

**Description:**
Returns recent throughput metrics.

**Response Example:**
```json
{
"metric": "current_throughput",
"records_last_window": 5200,
"window_minutes": 60
}
```
---

### GET /metrics/current/late-data

**Description:**
Returns recent late data metrics.

**Response Example:**
```json
{
"metric": "current_late_data",
"late_records": 120,
"late_percentage": 2.3
}
```
---

### GET /metrics/current/quarantine

**Description:**
Returns recent data quality metrics.

**Response Example:**
```json
{
"metric": "current_quarantine",
"invalid_records": 85
}
```
---

## 🔄 Data Refresh Model

- Metrics are updated via batch processing scripts:
    - `initial_load_metrics.py`
    - `incremental_load_metrics.py`

- API reflects the latest available metric artifacts

---

## ⚠️ Error Handling

Typical responses:

### 404 Not Found
Returned when a metric file does not exist

{
"detail": "Metric not found"
}

---

### 500 Internal Server Error
Returned when metric data cannot be read or parsed

{
"detail": "Internal server error"
}

---

## 🔐 Security Considerations

- API does not expose raw data sources
- Only aggregated metrics are returned
- Intended to sit behind:
    - API Gateway
    - Authentication layer (future enhancement)

---

## 🚧 Future Enhancements

- Query parameters (time range filtering)
- Pagination for time-series data
- Authentication / authorization
- OpenAPI schema expansion
- Versioned endpoints (e.g., /v1/metrics)

---

## 📎 Summary

The API layer provides:

- A stable interface to pipeline metrics
- Decoupling between frontend and backend processing
- Fast access to precomputed, reliable data

It represents the **contract layer** of the Hybrid Metrics Platform.