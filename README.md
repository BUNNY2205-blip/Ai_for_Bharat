# MindLearn AI Backend

FastAPI backend for AI-driven learning intelligence with:
- Concept weakness prediction
- Burnout risk prediction
- Unified analysis with readiness score and recommendations

## API Versioning

- Current stable contract is under `/api/v1`.
- Root `/` is reserved for service metadata and navigation.
- Future breaking changes will be introduced under `/api/v2` without disrupting v1 clients.

## Run

```bash
uvicorn backend.main:app --reload
```

## Endpoints

- `GET /`
- `GET /api/v1/health`
- `POST /api/v1/predict/weakness`
- `POST /api/v1/predict/burnout`
- `POST /api/v1/predict/analysis`

## Test `/api/v1/predict/analysis` with curl

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/predict/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "accuracy": 60,
    "attempts": 10,
    "avg_time": 30,
    "difficulty": 2,
    "repeated_errors": 3,
    "accuracy_trend": -8.5,
    "time_increase": 12,
    "consistency": 0.4,
    "study_hours": 7
  }'
```

## Test `/api/v1/predict/analysis` with httpie

```bash
http POST :8000/api/v1/predict/analysis \
  accuracy:=60 \
  attempts:=10 \
  avg_time:=30 \
  difficulty:=2 \
  repeated_errors:=3 \
  accuracy_trend:=-8.5 \
  time_increase:=12 \
  consistency:=0.4 \
  study_hours:=7
```
