"""Tests for the shared community usage counter (komarev) and cat milestones."""

import pytest

from web import state as state_mod
from web.state import _cat_emoji_for, _cat_title_for, _fetch_community_count


@pytest.mark.parametrize(
    ("count", "title"),
    [
        (0, "Curious Kitten"),
        (9, "Curious Kitten"),
        (10, "Happy Cat"),
        (24, "Happy Cat"),
        (25, "Grinning Cat"),
        (50, "Prowling Cat"),
        (99, "Prowling Cat"),
        (100, "Shadow Cat"),
        (250, "Lion Mode"),
        (500, "Tiger Analyst"),
        (999, "Tiger Analyst"),
        (1000, "Legendary Leopard"),
        (5000, "Legendary Leopard"),
    ],
)
def test_cat_title_thresholds(count: int, title: str):
    assert _cat_title_for(count) == title


def test_cat_emoji_matches_title_tier():
    # Each tier returns a non-empty emoji and the kitten default at zero.
    assert _cat_emoji_for(0) == "\U0001f431"
    assert _cat_emoji_for(1000) == "\U0001f406"
    assert all(_cat_emoji_for(c) for c in (0, 10, 25, 50, 100, 250, 500, 1000))


def _reset_cache():
    state_mod._community_count_cache["count"] = 0
    state_mod._community_count_cache["fetched_at"] = 0.0


class _FakeResp:
    def __init__(self, text: str):
        self.text = text


def test_fetch_parses_last_number(monkeypatch):
    _reset_cache()
    svg = "<svg><text>Repo Views</text><text>0</text><text>1515</text></svg>"
    monkeypatch.setattr(state_mod.httpx, "get", lambda *a, **k: _FakeResp(svg))
    assert _fetch_community_count() == 1515


def test_fetch_parses_thousands_separator(monkeypatch):
    _reset_cache()
    # komarev formats large counts with a comma, e.g. >1,515</text>
    svg = '<text>Repo Views</text><text x="93.5" y="14">1,515</text>'
    monkeypatch.setattr(state_mod.httpx, "get", lambda *a, **k: _FakeResp(svg))
    assert _fetch_community_count() == 1515


def test_fetch_caches_within_window(monkeypatch):
    _reset_cache()
    monkeypatch.setattr(state_mod.httpx, "get", lambda *a, **k: _FakeResp("<text>42</text>"))
    assert _fetch_community_count() == 42

    # Second call within 30s must hit cache, not the (now-raising) network.
    def _boom(*a, **k):
        raise AssertionError("network should not be hit within cache window")

    monkeypatch.setattr(state_mod.httpx, "get", _boom)
    assert _fetch_community_count() == 42


def test_fetch_returns_cached_on_error(monkeypatch):
    _reset_cache()
    state_mod._community_count_cache["count"] = 7

    def _raise(*a, **k):
        raise RuntimeError("boom")

    monkeypatch.setattr(state_mod.httpx, "get", _raise)
    assert _fetch_community_count() == 7
