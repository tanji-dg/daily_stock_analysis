# -*- coding: utf-8 -*-
"""Regression tests for Japan market review support and the `ja` report language."""

import pytest

from src.report_language import (
    SUPPORTED_REPORT_LANGUAGES,
    get_report_labels,
    get_sentiment_label,
    get_signal_level,
    is_supported_report_language_value,
    localize_confidence_level,
    localize_operation_advice,
    localize_trend_prediction,
    normalize_report_language,
)
from src.market_context import get_market_guidelines, get_market_role
from src.core.market_profile import JP_PROFILE, get_profile
from src.core.market_strategy import JP_BLUEPRINT, get_market_strategy_blueprint


def test_ja_is_supported_and_normalized() -> None:
    assert "ja" in SUPPORTED_REPORT_LANGUAGES
    assert normalize_report_language("ja") == "ja"
    assert normalize_report_language("jp") == "ja"
    assert normalize_report_language("japanese") == "ja"
    assert normalize_report_language("ja-JP") == "ja"
    assert is_supported_report_language_value("ja")
    assert is_supported_report_language_value("jp")
    # 既存言語は回帰なし
    assert normalize_report_language("en") == "en"
    assert normalize_report_language("zh") == "zh"


def test_ja_report_labels_cover_all_keys() -> None:
    zh = get_report_labels("zh")
    ja = get_report_labels("ja")
    assert set(zh) == set(ja)
    assert ja["buy_label"] == "買い"
    assert ja["report_title"] == "株式分析レポート"


def test_ja_localizers_round_trip() -> None:
    assert localize_operation_advice("买入", "ja") == "買い"
    assert localize_operation_advice("strong buy", "ja") == "強い買い"
    assert localize_trend_prediction("看多", "ja") == "強気"
    assert localize_confidence_level("高", "ja") == "高い"
    text, _emoji, tag = get_signal_level("买入", 70, "ja")
    assert text == "買い" and tag == "buy"


def test_ja_sentiment_labels() -> None:
    assert get_sentiment_label(90, "ja") == "非常に楽観"
    assert get_sentiment_label(50, "ja") == "中立"
    assert get_sentiment_label(5, "ja") == "非常に悲観"


def test_market_context_ja_roles_and_guidelines() -> None:
    assert get_market_role("7203.T", "ja") == "日本株"
    assert get_market_role("AAPL", "ja") == "米国株"
    assert get_market_role("600519", "ja") == "中国A株"
    guidelines = get_market_guidelines("7203.T", "ja")
    assert "日本株" in guidelines and "円相場" in guidelines
    # 既存言語は回帰なし
    assert get_market_role("7203.T", "en") == "Japan stock"
    assert get_market_role("7203.T", "zh") == "日股"


def test_jp_market_profile_and_strategy() -> None:
    assert get_profile("jp") is JP_PROFILE
    assert JP_PROFILE.region == "jp"
    assert JP_PROFILE.mood_index_code == "N225"
    assert get_market_strategy_blueprint("jp") is JP_BLUEPRINT
    block = JP_BLUEPRINT.to_prompt_block()
    assert "日経225" in block
    assert "戦略フレームワーク" in JP_BLUEPRINT.to_markdown_block()


def test_compute_effective_region_handles_jp_and_keeps_both() -> None:
    from src.core.trading_calendar import compute_effective_region

    assert compute_effective_region("jp", {"jp"}) == "jp"
    assert compute_effective_region("jp", {"cn"}) == ""
    # 'both' は cn/hk/us のみ（日股が開いていても含めない）
    assert compute_effective_region("both", {"cn", "hk", "us", "jp"}) == "cn,hk,us"
    assert compute_effective_region("cn", {"cn"}) == "cn"


def test_resolve_market_review_regions_jp_standalone() -> None:
    from src.core.market_review import _resolve_market_review_regions

    assert _resolve_market_review_regions("jp") == ["jp"]
    assert _resolve_market_review_regions("both") == ["cn", "hk", "us"]
    assert _resolve_market_review_regions("cn,jp") == ["cn", "jp"]


def test_market_analyzer_accepts_jp_region() -> None:
    from src.market_analyzer import MarketAnalyzer

    analyzer = MarketAnalyzer(region="jp")
    assert analyzer.region == "jp"
    assert analyzer.profile.region == "jp"


@pytest.mark.parametrize("market", ["cn", "hk", "us", "jp"])
def test_market_light_regions_include_jp(market: str) -> None:
    from src.services.market_light_service import MARKET_LIGHT_REGIONS, normalize_market_region

    assert market in MARKET_LIGHT_REGIONS
    assert normalize_market_region(market) == market
