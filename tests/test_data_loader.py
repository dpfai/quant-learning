from datetime import datetime, timedelta, timezone

import pandas as pd

from utils.data_loader import DataLoader


def sample_ohlcv() -> pd.DataFrame:
    index = pd.date_range("2024-01-01", periods=5, freq="D")
    return pd.DataFrame(
        {
            "Open": [100, 101, 102, 103, 104],
            "High": [101, 102, 103, 104, 105],
            "Low": [99, 100, 101, 102, 103],
            "Close": [100.5, 101.5, 102.5, 103.5, 104.5],
            "Adj Close": [100.5, 101.5, 102.5, 103.5, 104.5],
            "Volume": [1000, 1100, 1200, 1300, 1400],
        },
        index=index,
    )


def test_download_saves_and_reuses_cache(tmp_path, monkeypatch):
    calls = {"count": 0}

    def fake_download(*args, **kwargs):
        calls["count"] += 1
        return sample_ohlcv()

    monkeypatch.setattr("utils.data_loader.yf.download", fake_download)

    loader = DataLoader(cache_dir=str(tmp_path), max_age_hours=24)
    first = loader.download("SPY", period="1mo")
    second = loader.download("SPY", period="1mo")

    assert calls["count"] == 1
    assert first.equals(second)
    assert (tmp_path / "SPY_1mo.parquet").exists()


def test_download_batch_returns_each_ticker(tmp_path, monkeypatch):
    monkeypatch.setattr("utils.data_loader.yf.download", lambda *args, **kwargs: sample_ohlcv())

    loader = DataLoader(cache_dir=str(tmp_path))
    data = loader.download_batch(["SPY", "QQQ"], period="1mo")

    assert set(data) == {"SPY", "QQQ"}
    assert all(not df.empty for df in data.values())


def test_expired_cache_is_invalid(tmp_path):
    loader = DataLoader(cache_dir=str(tmp_path), max_age_hours=24)
    path = tmp_path / "SPY_1mo.parquet"
    sample_ohlcv().to_parquet(path)

    old_time = (datetime.now(timezone.utc) - timedelta(hours=48)).timestamp()
    path.touch()
    path.chmod(0o644)
    import os

    os.utime(path, (old_time, old_time))

    assert not loader.is_cache_valid("SPY", period="1mo")
