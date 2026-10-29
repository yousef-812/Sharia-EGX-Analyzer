from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.providers.base import CsvPriceProvider
from app.indicators import analyze_prices
from app.store import save_run, latest_runs

app = FastAPI(title="Sharia EGX Analyzer API", version="0.1.0", description="Experimental technical analysis API. Sharia screening is not inferred without a verified methodology.")
PRICES_DIR = Path(os.getenv("PRICES_DIR", "./data/prices"))
provider = CsvPriceProvider(PRICES_DIR)

class ScanRequest(BaseModel):
    symbols: list[str] = Field(default_factory=list, description="Symbols to scan; empty means all local CSV symbols")

@app.get("/health")
def health():
    return {"status": "ok", "service": "sharia-egx-analyzer", "data_provider": "local_csv"}

@app.get("/api/v1/universe")
def universe():
    return {"symbols": provider.symbols(), "count": len(provider.symbols()), "source": "local_csv_files"}

@app.get("/api/v1/analysis/{symbol}")
def analysis(symbol: str):
    try:
        result = analyze_prices(provider.load(symbol))
        result["symbol"] = symbol.upper()
        result["run_id"] = save_run(symbol, result)
        return result
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

@app.post("/api/v1/scan")
def scan(request: ScanRequest):
    symbols = [s.upper().strip() for s in request.symbols if s.strip()] or provider.symbols()
    results, errors = [], []
    for symbol in symbols:
        try:
            result = analyze_prices(provider.load(symbol))
            result["symbol"] = symbol
            result["run_id"] = save_run(symbol, result)
            results.append(result)
        except (FileNotFoundError, ValueError, KeyError) as exc:
            errors.append({"symbol": symbol, "error": str(exc)})
    return {"requested": len(symbols), "analyzed": len(results), "results": results, "errors": errors}

@app.get("/api/v1/runs/latest")
def runs_latest(limit: int = 20):
    if not 1 <= limit <= 200:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
    return {"runs": latest_runs(limit)}
