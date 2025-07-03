# Home Budget API

A Flask-based REST API for managing personal budgets: user registration, JWT auth, CRUD on categories and expenses, filtering, and spending stats.

## Quickstart

1. **Docker**
   ```bash
   docker-compose up --build
   ```
   API available at http://localhost:5000

2. **Without Docker**
   ```bash
   pip install -r requirements.txt
   export DATABASE_URL=postgresql://<user>:<pw>@localhost:5432/homebudget
   flask run
   ```

## API Docs
Browse interactive Swagger UI at http://localhost:5000/apidocs

## Testing
```bash
pytest
```

## Endpoints
| Path             | Method   | Auth | Description                |
|------------------|----------|------|----------------------------|
| /auth/register   | POST     | No   | Register new user          |
| /auth/login      | POST     | No   | Get JWT token              |
| /categories      | GET,POST | Yes  | List/Create categories     |
| /categories/<id> | DELETE   | Yes  | Delete category            |
| /expenses        | GET,POST | Yes  | List/Create expenses       |
| /expenses/<id>   | DELETE   | Yes  | Delete expense             |
| /expenses/stats  | GET      | Yes  | Spending stats             |
