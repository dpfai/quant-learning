"""Tests for JSON-backed watchlists."""

import pytest

from utils.watchlist_manager import WatchlistManager


def test_defaults_are_created(tmp_path):
    manager = WatchlistManager(str(tmp_path / "watchlists.json"))

    assert "ETFs" in manager.list_watchlists()
    assert "SPY" in manager.get_watchlist("ETFs")


def test_create_add_remove_and_delete_watchlist(tmp_path):
    manager = WatchlistManager(str(tmp_path / "watchlists.json"))

    manager.create_watchlist("Test", [" aapl ", "AAPL"])
    manager.add_ticker("Test", "msft")
    manager.remove_ticker("Test", "AAPL")

    assert manager.get_watchlist("Test") == ["MSFT"]

    manager.delete_watchlist("Test")
    assert "Test" not in manager.list_watchlists()


def test_duplicate_watchlist_is_rejected(tmp_path):
    manager = WatchlistManager(str(tmp_path / "watchlists.json"))
    manager.create_watchlist("Test")

    with pytest.raises(ValueError, match="already exists"):
        manager.create_watchlist("Test")
