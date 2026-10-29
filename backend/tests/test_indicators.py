import pandas as pd
from app.indicators import analyze_prices, validate_ohlcv


def sample_data(n=80):
    close = [10 + i * 0.1 for i in range(n)]
    return pd.DataFrame({"date": pd.date_range("2025-01-01", periods=n), "open": close, "high": [x + 0.2 for x in close], "low": [x - 0.2 for x in close], "close": close, "volume": [1000] * n})


def test_analysis_returns_indicator_fields():
    result = analyze_prices(sample_data())
    assert result["close"] > 0
    assert "rsi14" in result["indicators"]
    assert result["sharia_review"]["status"] == "not_assessed"
    assert result["indicator_33"]["status"] == "not_configured"


def test_validate_sorts_dates():
    data = sample_data().iloc[::-1]
    result = validate_ohlcv(data)
    assert result["date"].is_monotonic_increasing
