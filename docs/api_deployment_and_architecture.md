# REST API Deployment & System Architecture

## 1. System Topology
The decision engine exposes a high-throughput REST API using **FastAPI** and **Pydantic**:

```
[ Frontend / ERP (SAP, Blue Yonder) ]
                 │
                 ▼
       [ FastAPI Gateway ]
                 │
   ┌─────────────┴─────────────┐
   ▼                           ▼
[ Inventory Optimizer ]   [ Markdown Engine ]
   │                           │
   ▼                           ▼
[ Newsvendor & ROP ]      [ Decay Detector ]
   │                           │
   └─────────────┬─────────────┘
                 ▼
         [ JSON Response ]
```

## 2. API Endpoints
- `GET /health`: Health status.
- `GET /catalog`: Silhouette economics and lead-time profiles.
- `POST /optimize-inventory`: Accepts demand forecasts; returns $Q^*$, 60% pre-commitment, 40% chase buffer, and safety stock.
- `POST /evaluate-markdown`: Analyzes weekly velocity deceleration; returns recommended markdown stage and effective price.
- `GET /alerts`: Returns real-time flags for viral surges and trend decay.

## 3. Docker Deployment Specification
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```
