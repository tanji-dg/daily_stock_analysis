# -*- coding: utf-8 -*-
"""Market strategy blueprints for CN/HK/US/JP daily market recap."""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class StrategyDimension:
    """Single strategy dimension used by market recap prompts."""

    name: str
    objective: str
    checkpoints: List[str]


@dataclass(frozen=True)
class MarketStrategyBlueprint:
    """Region specific market strategy blueprint."""

    region: str
    title: str
    positioning: str
    principles: List[str]
    dimensions: List[StrategyDimension]
    action_framework: List[str]

    def to_prompt_block(self) -> str:
        """Render blueprint as prompt instructions."""
        principles_text = "\n".join([f"- {item}" for item in self.principles])
        action_text = "\n".join([f"- {item}" for item in self.action_framework])

        dims = []
        for dim in self.dimensions:
            checkpoints = "\n".join([f"  - {cp}" for cp in dim.checkpoints])
            dims.append(f"- {dim.name}: {dim.objective}\n{checkpoints}")
        dimensions_text = "\n".join(dims)

        return (
            f"## Strategy Blueprint: {self.title}\n"
            f"{self.positioning}\n\n"
            f"### Strategy Principles\n{principles_text}\n\n"
            f"### Analysis Dimensions\n{dimensions_text}\n\n"
            f"### Action Framework\n{action_text}"
        )

    def to_markdown_block(self) -> str:
        """Render blueprint as markdown section for template fallback report."""
        dims = "\n".join([f"- **{dim.name}**: {dim.objective}" for dim in self.dimensions])
        if self.region == "us":
            section_title = "### VI. Strategy Framework"
        elif self.region == "jp":
            section_title = "### 六、戦略フレームワーク"
        else:
            section_title = "### 六、策略框架"
        return f"{section_title}\n{dims}\n"


CN_BLUEPRINT = MarketStrategyBlueprint(
    region="cn",
    title="A股市场三段式复盘策略",
    positioning="聚焦指数趋势、资金博弈与板块轮动，形成次日交易计划。",
    principles=[
        "先看指数方向，再看量能结构，最后看板块持续性。",
        "结论必须映射到仓位、节奏与风险控制动作。",
        "判断使用当日数据与近3日新闻，不臆测未验证信息。",
    ],
    dimensions=[
        StrategyDimension(
            name="趋势结构",
            objective="判断市场处于上升、震荡还是防守阶段。",
            checkpoints=["上证/深证/创业板是否同向", "放量上涨或缩量下跌是否成立", "关键支撑阻力是否被突破"],
        ),
        StrategyDimension(
            name="资金情绪",
            objective="识别短线风险偏好与情绪温度。",
            checkpoints=["涨跌家数与涨跌停结构", "成交额是否扩张", "高位股是否出现分歧"],
        ),
        StrategyDimension(
            name="主线板块",
            objective="提炼可交易主线与规避方向。",
            checkpoints=["领涨板块是否具备事件催化", "板块内部是否有龙头带动", "领跌板块是否扩散"],
        ),
    ],
    action_framework=[
        "进攻：指数共振上行 + 成交额放大 + 主线强化。",
        "均衡：指数分化或缩量震荡，控制仓位并等待确认。",
        "防守：指数转弱 + 领跌扩散，优先风控与减仓。",
    ],
)

US_BLUEPRINT = MarketStrategyBlueprint(
    region="us",
    title="US Market Regime Strategy",
    positioning="Focus on index trend, macro narrative, and sector rotation to define next-session risk posture.",
    principles=[
        "Read market regime from S&P 500, Nasdaq, and Dow alignment first.",
        "Separate beta move from theme-driven alpha rotation.",
        "Translate recap into actionable risk-on/risk-off stance with clear invalidation points.",
    ],
    dimensions=[
        StrategyDimension(
            name="Trend Regime",
            objective="Classify the market as momentum, range, or risk-off.",
            checkpoints=[
                "Are SPX/NDX/DJI directionally aligned",
                "Did volume confirm the move",
                "Are key index levels reclaimed or lost",
            ],
        ),
        StrategyDimension(
            name="Macro & Flows",
            objective="Map policy/rates narrative into equity risk appetite.",
            checkpoints=[
                "Treasury yield and USD implications",
                "Breadth and leadership concentration",
                "Defensive vs growth factor rotation",
            ],
        ),
        StrategyDimension(
            name="Sector Themes",
            objective="Identify persistent leaders and vulnerable laggards.",
            checkpoints=[
                "AI/semiconductor/software trend persistence",
                "Energy/financials sensitivity to macro data",
                "Volatility signals from VIX and large-cap earnings",
            ],
        ),
    ],
    action_framework=[
        "Risk-on: broad index breakout with expanding participation.",
        "Neutral: mixed index signals; focus on selective relative strength.",
        "Risk-off: failed breakouts and rising volatility; prioritize capital preservation.",
    ],
)

HK_BLUEPRINT = MarketStrategyBlueprint(
    region="hk",
    title="港股市场三段式复盘策略",
    positioning="聚焦恒生指数趋势、南向资金博弈与板块轮动，形成次日交易计划。",
    principles=[
        "先看恒指/恒科/国企指数方向，再看南向资金情绪，最后看板块持续性。",
        "结论必须映射到仓位、节奏与风险控制动作。",
        "判断使用当日数据与近3日新闻，不臆测未验证信息。",
    ],
    dimensions=[
        StrategyDimension(
            name="趋势结构",
            objective="判断市场处于上升、震荡还是防守阶段。",
            checkpoints=["恒指/恒科/国企指数是否同向", "放量上涨或缩量下跌是否成立", "关键支撑阻力是否被突破"],
        ),
        StrategyDimension(
            name="资金情绪",
            objective="识别南向资金风险偏好与情绪温度。",
            checkpoints=["南向资金净流入方向与规模", "港元汇率与内地政策含义", "市场广度与龙头集中度"],
        ),
        StrategyDimension(
            name="主线板块",
            objective="提炼可交易主线与规避方向。",
            checkpoints=["科技/互联网平台趋势持续性", "金融/地产对政策转向的敏感度", "防御与成长因子轮动"],
        ),
    ],
    action_framework=[
        "进攻：恒指共振上行 + 南向资金持续流入 + 主线强化。",
        "均衡：指数分化或缩量震荡，控制仓位并等待确认。",
        "防守：指数转弱 + 波动率上升，优先风控与减仓。",
    ],
)


JP_BLUEPRINT = MarketStrategyBlueprint(
    region="jp",
    title="日本株市場 三段階リキャップ戦略",
    positioning="日経225/TOPIXのトレンド、海外投資家フロー、テーマ・セクター循環に着目し、翌営業日の取引計画を立てる。",
    principles=[
        "まず日経225/TOPIX/グロース市場の方向、次に海外投資家フロー、最後にセクターの持続性を見る。",
        "結論は必ずポジション・タイミング・リスク管理アクションに落とし込む。",
        "判断は当日データと直近3日のニュースに基づき、未確認情報を推測しない。",
    ],
    dimensions=[
        StrategyDimension(
            name="トレンド構造",
            objective="市場が上昇・もみ合い・守りのどの局面かを判断する。",
            checkpoints=["日経225/TOPIX/グロース市場が同方向か", "出来高を伴う上昇か縮小を伴う下落か", "主要な支持・抵抗を突破したか"],
        ),
        StrategyDimension(
            name="資金・心理",
            objective="海外投資家のリスク選好と市場心理の温度を見極める。",
            checkpoints=["海外投資家の売買動向と規模", "円相場と日銀・政策の含意", "市場の広がりと主力銘柄の集中度"],
        ),
        StrategyDimension(
            name="主力セクター",
            objective="取引対象となる主力テーマと回避方向を抽出する。",
            checkpoints=["半導体/輸出関連のトレンド持続性", "金融/不動産の金利感応度", "ディフェンシブとグロースの循環"],
        ),
    ],
    action_framework=[
        "攻め：指数が共振して上昇 + 出来高拡大 + 主力テーマ強化。",
        "均衡：指数の分化や縮小もみ合い、ポジションを抑え確認を待つ。",
        "守り：指数が弱含み + ボラティリティ上昇、リスク管理と縮小を優先。",
    ],
)


def get_market_strategy_blueprint(region: str) -> MarketStrategyBlueprint:
    """Return strategy blueprint by market region."""
    if region == "us":
        return US_BLUEPRINT
    if region == "hk":
        return HK_BLUEPRINT
    if region == "jp":
        return JP_BLUEPRINT
    return CN_BLUEPRINT
