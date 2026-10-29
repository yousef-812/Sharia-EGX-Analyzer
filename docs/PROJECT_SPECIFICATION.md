# Project Specification — Sharia EGX Analyzer

## 1. Purpose
Build an Arabic-first research tool that analyzes Egyptian Exchange (EGX) stocks using daily OHLCV data and transparent technical indicators. A separate, documented Sharia-screening workflow must be used for any Sharia-related status. Technical price patterns are not evidence of Sharia compliance.

## 2. Core users and workflows
- Enter one EGX symbol and view the latest available analysis.
- Scan every symbol for which valid local data is available.
- Review prior scan runs and compare results over time.
- Inspect indicator values, data date, and methodology/provenance.
- Review Sharia-screening status separately, including source and effective date once a verified methodology is configured.

## 3. Functional requirements
### Market data
- Accept daily OHLCV records: date, open, high, low, close, volume.
- Validate numeric values, dates, duplicate sessions, candle consistency, missing fields, and nonnegative volume.
- Record provider/source, retrieval timestamp, and any adjustments when a production provider is integrated.
- Only use market data obtained through an authorized source. The current implementation reads local CSV files and does not scrape EGX or connect to a live provider.

### Technical analysis
- Starter indicators: EMA 20, EMA 50, MACD (12, 26, 9), and RSI (14).
- Return raw values, analysis date, and a simple transparent heuristic summary.
- Label the score as experimental; do not imply it predicts profits.
- Planned extensions: ATR, MFI, ADX, volume/relative-volume signals, support/resistance, volatility and liquidity filters.
- Any strategy must be evaluated with out-of-sample testing and realistic fees, taxes, slippage, and execution assumptions before practical use.

### Sharia screening
- Do not classify a stock as compliant/non-compliant unless an approved screening standard and verified, current company financial data are supplied.
- Store the standard name/version, data source, screening date, thresholds, result, reviewer, and rationale.
- Display “not assessed” when required information is absent or stale.
- Never derive Sharia status from technical indicators or price movement.

### Indicator 33
- Exact formula, thresholds, interpretation, and source are currently unknown.
- It is deliberately marked not_configured.
- Do not implement or estimate the formula until the owner provides its definition and sample cases for validation.

### Scans and history
- Scan one or more symbols, or all symbols present in the local data directory.
- Store each analysis with a timestamp and symbol.
- Return per-symbol errors without discarding successful results.
- Planned: post-close scheduler using Egypt local time and the official market calendar, retry/backoff, alerts, run locking, and job audit logs.

## 4. API (starter)
- GET /health — service health.
- GET /api/v1/universe — symbols found in local CSV files.
- GET /api/v1/analysis/{symbol} — analyze one symbol and save the result.
- POST /api/v1/scan — scan provided symbols, or all local symbols when omitted.
- GET /api/v1/runs/latest?limit=20 — recent saved results.

These endpoints are a development baseline, not a production-ready public API.

## 5. Mobile application
- Flutter, Arabic-first right-to-left layout.
- Enter a symbol and request analysis.
- Show close, analysis date, technical summary, EMA, MACD and RSI.
- Clearly show Sharia status as not assessed and Indicator 33 as not configured until valid definitions/data are integrated.
- Planned screens: market overview, scan results, symbol details, run history, methodology/source details, settings and disclaimer.

## 6. Architecture
- Flutter mobile client.
- FastAPI backend.
- Provider interface; current provider is local CSV.
- SQLite for development run history.
- Future production deployment should use a managed database, background worker/scheduler, authenticated API, rate limiting, structured logs, monitoring, and secrets management.

## 7. Security and reliability
- Never commit API keys, passwords, account credentials, or production secrets.
- Validate inputs and cap request sizes.
- Add authentication and rate limits before exposing write-heavy endpoints publicly.
- Keep audit trails for data-source changes and screening methodology changes.
- Handle stale/missing data explicitly; do not silently treat missing values as a negative signal.
- Add unit, integration, API contract, and data-quality tests.

## 8. Milestones
1. Starter API, CSV provider, basic indicators, local history, Flutter starter.
2. Confirm Indicator 33 definition and document screening standard.
3. Select and authorize a reliable EGX data provider; add provenance and corporate-action handling.
4. Implement post-close scheduling, retries, run history filters and alerts.
5. Build full mobile overview, scan, details and history screens.
6. Backtesting, fees/slippage, benchmark comparison, out-of-sample validation.
7. Security review, monitoring, deployment and operational documentation.

## 9. Acceptance criteria
- Invalid OHLCV files are rejected with understandable errors.
- Valid CSV data produces reproducible indicator values.
- API reports missing symbols clearly and preserves successful scan results.
- Each saved run includes symbol and timestamp.
- Missing Sharia evidence produces “not assessed”, not a guessed result.
- Indicator 33 remains disabled until its formula/source are confirmed.
- User-facing screens include a clear experimental/research disclaimer.

## 10. Disclaimer
This project is for educational and research use only. It is not investment advice, does not guarantee performance, and it does not itself issue a religious ruling. Verify data, strategy results, and Sharia methodology with qualified professionals before relying on outputs.
