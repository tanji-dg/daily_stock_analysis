# -*- coding: utf-8 -*-
"""
Market context detection for LLM prompts.

Detects the market (A-shares, HK, US) from a stock code and returns
market-specific role descriptions so prompts are not hardcoded to a
single market.

Fixes: https://github.com/ZhuLinsen/daily_stock_analysis/issues/644
"""

import re
from typing import Optional


def detect_market(stock_code: Optional[str]) -> str:
    """Detect market from stock code.

    Returns:
        One of 'cn', 'hk', 'us', or 'cn' as fallback.
    """
    if not stock_code:
        return "cn"

    code = stock_code.strip().upper()

    # HK stocks: HK00700, 00700.HK, or 5-digit pure numbers
    if code.startswith("HK") or code.endswith(".HK"):
        return "hk"
    lower = code.lower()
    if lower.endswith(".hk"):
        return "hk"
    # 5-digit pure numbers are HK (A-shares are 6-digit)
    if code.isdigit() and len(code) == 5:
        return "hk"

    # Japan/Korea suffix-only symbols supported by Yahoo Finance.
    # Bare Korean six-digit codes remain A-share fallback to avoid collision.
    # Japan Yahoo suffix (.T). Also accepts new alphanumeric TSE codes
    # (e.g. 285A = Kioxia): first char a digit, rest digits/uppercase, length 4-5.
    if re.match(r'^[0-9][0-9A-Z]{3,4}\.T$', code):
        return "jp"
    if re.match(r'^\d{6}\.(KS|KQ)$', code):
        return "kr"

    # US stocks: 1-5 uppercase letters (AAPL, TSLA, GOOGL)
    # Also handles suffixed forms like BRK.B
    if re.match(r'^[A-Z]{1,5}(\.[A-Z]{1,2})?$', code):
        return "us"

    # Default: A-shares (6-digit numbers like 600519, 000001)
    return "cn"


# -- Market-specific role descriptions --

_MARKET_ROLES = {
    "cn": {
        "zh": " A 股",
        "en": "China A-shares",
        "ja": "中国A株",
    },
    "hk": {
        "zh": "港股",
        "en": "Hong Kong stock",
        "ja": "香港株",
    },
    "us": {
        "zh": "美股",
        "en": "US stock",
        "ja": "米国株",
    },
    "jp": {
        "zh": "日股",
        "en": "Japan stock",
        "ja": "日本株",
    },
    "kr": {
        "zh": "韩股",
        "en": "Korea stock",
        "ja": "韓国株",
    },
}

_MARKET_GUIDELINES = {
    "cn": {
        "zh": (
            "- 本次分析对象为 **A 股**（中国沪深交易所上市股票）。\n"
            "- 请关注 A 股特有的涨跌停机制（±10%/±20%/±30%）、T+1 交易制度及相关政策因素。"
        ),
        "en": (
            "- This analysis covers a **China A-share** (listed on Shanghai/Shenzhen exchanges).\n"
            "- Consider A-share-specific rules: daily price limits (±10%/±20%/±30%), T+1 settlement, and PRC policy factors."
        ),
        "ja": (
            "- 今回の分析対象は **中国A株**（上海・深セン取引所の上場銘柄）です。\n"
            "- A株特有の値幅制限（±10%/±20%/±30%）、T+1決済、中国の政策要因に留意してください。"
        ),
    },
    "hk": {
        "zh": (
            "- 本次分析对象为 **港股**（香港交易所上市股票）。\n"
            "- 港股无涨跌停限制，支持 T+0 交易，需关注港币汇率、南北向资金流及联交所特有规则。"
        ),
        "en": (
            "- This analysis covers a **Hong Kong stock** (listed on HKEX).\n"
            "- HK stocks have no daily price limits, allow T+0 trading. Consider HKD FX, Southbound/Northbound flows, and HKEX-specific rules."
        ),
        "ja": (
            "- 今回の分析対象は **香港株**（香港取引所の上場銘柄）です。\n"
            "- 香港株は値幅制限がなくT+0取引が可能です。香港ドル相場、南向き・北向き資金フロー、HKEX特有のルールに留意してください。"
        ),
    },
    "us": {
        "zh": (
            "- 本次分析对象为 **美股**（美国交易所上市股票）。\n"
            "- 美股无涨跌停限制（但有熔断机制），支持 T+0 交易和盘前盘后交易，需关注美元汇率、美联储政策及 SEC 监管动态。"
        ),
        "en": (
            "- This analysis covers a **US stock** (listed on NYSE/NASDAQ).\n"
            "- US stocks have no daily price limits (but have circuit breakers), allow T+0 and pre/after-market trading. Consider USD FX, Fed policy, and SEC regulations."
        ),
        "ja": (
            "- 今回の分析対象は **米国株**（NYSE/NASDAQ の上場銘柄）です。\n"
            "- 米国株は値幅制限がなく（ただしサーキットブレーカーあり）、T+0や時間外取引が可能です。米ドル相場、FRBの政策、SECの規制動向に留意してください。"
        ),
    },
    "jp": {
        "zh": (
            "- 本次分析对象为 **日股**（日本交易所上市股票，Yahoo Finance suffix 如 `.T`）。\n"
            "- 请按日本市场语境分析，关注日元汇率、日本央行政策、公司治理与行业周期；不要套用 A 股涨跌停、北向资金、龙虎榜、融资融券等 A 股专属概念。"
        ),
        "en": (
            "- This analysis covers a **Japan stock** (Yahoo Finance suffix such as `.T`).\n"
            "- Use Japan-market context: JPY FX, BOJ policy, corporate governance, and sector cycles; do not apply China A-share concepts such as daily price-limit boards, Northbound flows, Dragon Tiger lists, or margin-financing narratives."
        ),
        "ja": (
            "- 今回の分析対象は **日本株**（日本の取引所の上場銘柄、Yahoo Finance では `.T` などのサフィックス）です。\n"
            "- 日本市場の文脈で分析し、円相場、日銀の政策、コーポレートガバナンス、業種サイクルに留意してください。A株特有の値幅制限ボード、北向き資金、龍虎榜、信用取引の語り口などをそのまま当てはめないこと。"
        ),
    },
    "kr": {
        "zh": (
            "- 本次分析对象为 **韩股**（韩国交易所/KOSDAQ 上市股票，必须带 `.KS` / `.KQ` 后缀）。\n"
            "- 请按韩国市场语境分析，关注韩元汇率、韩国央行政策、半导体/互联网产业周期与韩国交易制度；不要套用 A 股涨跌停、北向资金、龙虎榜、融资融券等 A 股专属概念。"
        ),
        "en": (
            "- This analysis covers a **Korea stock** (KOSPI/KOSDAQ suffix `.KS` / `.KQ`).\n"
            "- Use Korea-market context: KRW FX, Bank of Korea policy, semiconductor/internet cycles, and local trading rules; do not apply China A-share concepts such as daily price-limit boards, Northbound flows, Dragon Tiger lists, or margin-financing narratives."
        ),
        "ja": (
            "- 今回の分析対象は **韓国株**（KOSPI/KOSDAQ、`.KS` / `.KQ` サフィックス付き）です。\n"
            "- 韓国市場の文脈で分析し、ウォン相場、韓国銀行の政策、半導体・インターネット産業のサイクル、現地の取引制度に留意してください。A株特有の値幅制限ボード、北向き資金、龍虎榜、信用取引の語り口などをそのまま当てはめないこと。"
        ),
    },
}


def _resolve_lang_key(lang: Optional[str]) -> str:
    """Map a report-language code to a market-context label key (zh/en/ja)."""
    normalized = str(lang or "zh").strip().lower()
    if normalized.startswith("en"):
        return "en"
    if normalized.startswith("ja") or normalized.startswith("jp"):
        return "ja"
    return "zh"


def get_market_role(stock_code: Optional[str], lang: str = "zh") -> str:
    """Return market-specific role description for LLM prompt.

    Args:
        stock_code: The stock code being analyzed.
        lang: 'zh' or 'en'.

    Returns:
        Role string like 'A 股投资分析' or 'US stock investment analysis'.
    """
    market = detect_market(stock_code)
    lang_key = _resolve_lang_key(lang)
    role = _MARKET_ROLES.get(market, _MARKET_ROLES["cn"])
    return role.get(lang_key, role["zh"])


def get_market_guidelines(stock_code: Optional[str], lang: str = "zh") -> str:
    """Return market-specific analysis guidelines for LLM prompt.

    Args:
        stock_code: The stock code being analyzed.
        lang: 'zh' or 'en'.

    Returns:
        Multi-line string with market-specific guidelines.
    """
    market = detect_market(stock_code)
    lang_key = _resolve_lang_key(lang)
    guidelines = _MARKET_GUIDELINES.get(market, _MARKET_GUIDELINES["cn"])
    return guidelines.get(lang_key, guidelines["zh"])
