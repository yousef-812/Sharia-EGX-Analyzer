# Architecture

## Components

- **Flutter mobile client:** Arabic-first interface; calls the backend API.
- **FastAPI backend:** validates OHLCV data, calculates technical indicators, runs scans, and exposes history.
- **CSV provider (starter):** reads locally supplied, authorized OHLCV data. A licensed provider adapter can replace it later.
- **SQLite history:** stores timestamped analysis outputs for development.

## Data flow

1. Import validated daily OHLCV data.
2. Validate dates, prices, volume, and candle consistency.
3. Calculate technical indicators from historical bars.
4. Return technical summary separately from Sharia review.
5. Save each analysis run for comparison and later backtesting.

## Trust boundaries

Technical analysis cannot determine Sharia compliance. Sharia screening needs a documented standard, verified company financial data, a review date, and ideally qualified review. “Indicator 33” stays unimplemented until its exact formula and source are provided.

## Next architecture steps

- Add provider interface for licensed market data.
- Add authentication, rate limiting, audit logs, and deployment secrets management before public hosting.
- Add background scheduler only after provider, market calendar, timezone, and retry behavior are defined.
- Store raw-data provenance and methodology versions alongside each result.
