from __future__ import annotations

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {"date", "open", "high", "low", "close", "volume"}


def validate_ohlcv(frame: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    data = frame.copy()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    for col in ("open", "high", "low", "close", "volume"):
        data[col] = pd.to_numeric(data[col], errors="raise")
    data = data.sort_values("date").drop_duplicates("date").reset_index(drop=True)
    if data.empty:
        raise ValueError("No price rows supplied")
    if (data[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("OHLC prices must be positive")
    if (data["volume"] < 0).any():
        raise ValueError("Volume cannot be negative")
    if (data["high"] < data[["open", "close", "low"]].max(axis=1)).any():
        raise ValueError("High must be at least open, close, and low")
    if (data["low"] > data[["open", "close", "high"]].min(axis=1)).any():
        raise ValueError("Low must be at most open, close, and high")
    return data


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    result = 100 - (100 / (1 + rs))
    return result.where(loss.ne(0), 100).where(gain.ne(0) | loss.ne(0), 50)


def analyze_prices(frame: pd.DataFrame) -> dict:
    data = validate_ohlcv(frame)
    close = data["close"]
    ema20 = close.ewm(span=20, adjust=False).mean()
    ema50 = close.ewm(span=50, adjust=False).mean()
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    rsi_values = rsi(close)
    last = data.iloc[-1]
    score = 0
    score += 1 if last["close"] > ema20.iloc[-1] else -1
    score += 1 if ema20.iloc[-1] > ema50.iloc[-1] else -1
    score += 1 if macd.iloc[-1] > signal.iloc[-1] else -1
    current_rsi = rsi_values.iloc[-1]
    if pd.notna(current_rsi):
        score += 1 if 50 <= current_rsi < 70 else (-1 if current_rsi < 40 or current_rsi >= 70 else 0)
    label = "positive" if score >= 2 else "negative" if score <= -2 else "mixed"
    return {
        "symbol": None,
        "as_of": last["date"].date().isoformat(),
        "close": float(last["close"]),
        "volume": int(last["volume"]),
        "indicators": {
            "ema20": float(ema20.iloc[-1]), "ema50": float(ema50.iloc[-1]),
            "macd": float(macd.iloc[-1]), "macd_signal": float(signal.iloc[-1]),
            "rsi14": None if pd.isna(current_rsi) else float(current_rsi),
        },
        "technical_score": score,
        "technical_summary": label,
        "sharia_review": {"status": "not_assessed", "methodology": None, "note": "No Sharia status is inferred from technical price data. Add a verified screening source and documented methodology."},
        "indicator_33": {"status": "not_configured", "value": None, "note": "Formula and source must be specified before implementation."},
    }
