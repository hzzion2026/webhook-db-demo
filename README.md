# SQL Injection Webhook Scanner

A production-grade real-time webhook receiver that ingests incoming HTTP requests, validates payloads, and cross-references data against a PostgreSQL database using fuzzy text matching.

## Project Overview

| Attribute | Detail |
|-----------|--------|
| Type | Backend API Service |
| Protocol | REST (JSON Webhook) |
| Pattern | Request -> Validate -> Query -> Respond |
| Deployment | Docker Compose (App + PostgreSQL) |

## Technical Stack

| Layer | Technology |
|-------|-----------|
| Framework | FastAPI (Python 3.11) |
| Database | PostgreSQL 15 |
| Async Driver | asyncpg |
| Validation | Pydantic v2 |
| Container | Docker + Docker Compose |
| Testing | pytest + httpx |

## How It Works

Client sends a webhook payload to `POST /webhook`. The request is validated using Pydantic v2 models, then processed against the PostgreSQL database using trigram-based fuzzy search (ILIKE + pg_trgm). A structured JSON response is returned with matched results.

## Key Features

- Async endpoint with non-blocking IO via asyncpg + asyncio
- PostgreSQL trigram indexes for partial/approximate matching
- Pydantic v2 strict request/response validation
- Single `docker-compose up` brings up app + database
- Auto-migration with schema.sql on first startup
- Health check endpoint for uptime monitoring
- Graceful degradation when DB is unavailable
- Comprehensive async pytest test suite

## Quick Start

```bash
git clone https://github.com/hzzion2026/sql-injection-webhook-scanner.git
cd sql-injection-webhook-scanner
docker-compose up --build
```
