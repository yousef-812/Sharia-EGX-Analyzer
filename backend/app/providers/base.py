from __future__ import annotations

from pathlib import Path
import pandas as pd
from app.indicators import validate_ohlcv


class CsvPriceProvider:
    """Read locally supplied OHLCV CSV files; no network scraping is performed."""
    def __init__(self, prices_dir: str | Path = "data/prices"):
        self.prices_dir = Path(prices_dir)

    def symbols(self) -> list[str]:
        if not self.prices_dir.exists():
            return []
        return sorted(p.stem.upper() for p in self.prices_dir.glob("*.csv"))

    def load(self, symbol: str) -> pd.DataFrame:
        path = self.prices_dir / f"{symbol.upper()}.csv"
        if not path.exists():
            raise FileNotFoundError(f"No CSV price file for symbol {symbol.upper()}")
        return validate_ohlcv(pd.read_csv(path))
