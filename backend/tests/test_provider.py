import pandas as pd
import pytest
from app.indicators import validate_ohlcv


def test_missing_columns_raise():
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_ohlcv(pd.DataFrame({"date": ["2025-01-01"]}))
