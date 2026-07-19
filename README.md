# Polymarket Trading Bot

Automated trading system for Polymarket prediction markets, deployable on Google Cloud Run.

## Milestone 1: Project Foundation

Current scope includes:

- FastAPI application skeleton
- JSON structured logging (Google Cloud Logging compatible)
- `GET /` system information endpoint
- `GET /health` health check endpoint

## Local Development

### Prerequisites

- Python 3.12+
- pip

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Verify

```bash
curl http://localhost:8000/
curl http://localhost:8000/health
pytest
ruff check .
black --check .
```

## Project Structure

```
app/
├── api/routes.py      # HTTP endpoints
├── core/              # Config, logging, constants, security
└── main.py            # FastAPI entry point
tests/
└── test_api.py
```

## License

Private project.
