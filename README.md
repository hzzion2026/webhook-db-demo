# Webhook & Database Integration Demo

A Python **FastAPI** service that receives SMS/webhook messages, queries a **PostgreSQL** database for product information, and returns structured replies. Built for production-readiness with async IO, typed models, tests, and Docker.

---

## Architecture

```
SMS Gateway ──POST /webhook──> FastAPI App ──SQL──> PostgreSQL
                                      │
                                      └── JSON Response ──> Client
```

## Features

- **FastAPI** async endpoint (`POST /webhook`)
- **PostgreSQL** integration via `asyncpg` with fuzzy product search
- **Pydantic v2** models for request/response validation
- **Comprehensive test suite** (pytest + httpx)
- **Docker Compose** setup with auto-migration (schema.sql)
- **Health check** endpoint
- Structured logging and error handling

## Quick Start

### Option A: Docker (recommended)

```bash
docker-compose up --build
# API available at http://localhost:8000
```

### Option B: Local

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start PostgreSQL (adjust DATABASE_URL in app.py)
#    Then run schema.sql against it

# 3. Start the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### `POST /webhook`

Receive a webhook message and look up matching products.

**Request:**
```json
{
  "message_id": "msg-001",
  "sender": "+1234567890",
  "text": "keyboard",
  "timestamp": "2026-06-14T10:30:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "reply": "Found 2 products: Mechanical Keyboard RGB, Ergonomic Mouse Pad",
  "products": [
    {
      "product_id": 4,
      "name": "Mechanical Keyboard RGB",
      "price": 89.99,
      "stock": 80,
      "description": "Cherry MX Blue switches, full-size, per-key RGB lighting"
    }
  ]
}
```

### `GET /health`

```json
{ "status": "ok" }
```

## Running Tests

```bash
pytest tests/ -v --asyncio-mode=auto
```

Or with Make:

```bash
make test
```

## Project Structure

```
webhook-db-demo/
├── app.py              # FastAPI application
├── schema.sql          # PostgreSQL schema + seed data
├── Dockerfile          # Container build
├── docker-compose.yml  # App + PostgreSQL
├── requirements.txt    # Python dependencies
├── Makefile            # Common commands
├── tests/
│   ├── __init__.py
│   └── test_app.py     # Async test suite
└── README.md
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Python) |
| Database | PostgreSQL 15 |
| Async Driver | asyncpg |
| Validation | Pydantic v2 |
| Testing | pytest + httpx |
| Containerization | Docker + Docker Compose |
