# Sharia EGX Analyzer

An experimental Egyptian Exchange (EGX) stock-analysis project combining technical indicators with a configurable Sharia-compliance review workflow.

> **Important:** This project is for research and education, not investment advice or a religious ruling. Technical signals are not guarantees. Sharia status must be based on a documented, authoritative methodology and reviewed data. The formula/source for “Indicator 33” is intentionally not assumed.

## Project layout

- `backend/` — FastAPI service, CSV OHLCV ingestion, indicators, scan endpoints, SQLite run history.
- `mobile/` — Flutter starter app with Arabic-first UI.
- `docs/` — architecture, strategy, and implementation roadmap.
- `.github/workflows/` — backend test workflow.

## Quick start (backend)

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API documentation.

The starter uses CSV files for price data. It does not scrape EGX or connect to a paid data provider automatically. Only use data you are authorized to access.

## CSV format

Place files in `backend/data/prices/` named like `COMI.csv`, with columns:

`date,open,high,low,close,volume`

Dates should be ISO formatted (`YYYY-MM-DD`); prices and volume must be numeric.

## Run tests

```bash
cd backend
pytest
```

## Planned work

1. Confirm the exact “Indicator 33” formula and source.
2. Define the approved Sharia screening standard and review date/versioning.
3. Add a licensed EGX market-data provider.
4. Add post-close scheduling, robust scan history, and backtesting.
5. Expand the Flutter app and secure deployment configuration.

## Disclaimer

This software is experimental. It does not guarantee Sharia compliance, profitability, or accuracy. Verify market data and consult qualified financial and Sharia experts before relying on any output.