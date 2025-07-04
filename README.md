# HomeBudget API

This guide walks you through running the HomeBudget API with Docker Compose and accessing the built‑in Swagger documentation.

---

## Prerequisites

* Docker installed
* Docker Compose installed

---

## Project Layout

```
homebudget/
  ├── __init__.py
  ├── config.py
  ├── models/
  ├── routes/
  ├── schemas.py
  ├── static/
  └── ...
tests/
Dockerfile
requirements.txt
docker-compose.yml
README.md
```

---

## Environment Variables

Configured in `docker-compose.yml`:

* `DATABASE_URL`
* `JWT_SECRET`
* `FLASK_APP`
* `FLASK_ENV`

---

## Docker Compose Commands

### 1. Build & Start Services

```bash
docker-compose up --build -d
```

### 2. Check Status

```bash
docker-compose ps
```

### 3. Stream Logs

```bash
docker-compose logs -f web
```

### 4. Stop Services

```bash
docker-compose down
```

### 5. Full Teardown

```bash
docker-compose down -v
```

---

## Running Tests

```bash
docker-compose run --rm web pytest -q
```

---

## Accessing the API

* Base URL: `http://localhost:5000`
* Swagger UI: `http://localhost:5000/apidocs/`

---

## Database Reset

```bash
docker-compose down -v
docker-compose up --build -d
```

