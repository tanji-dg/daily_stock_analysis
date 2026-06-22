import type {
  AnalysisPhase,
  MarketPhaseSummary,
  MarketPhaseValue,
  ReportLanguage,
} from '../types/analysis';
import { normalizeReportLanguage } from './reportLanguage';

const REQUEST_PHASE_LABELS: Record<ReportLanguage, Record<AnalysisPhase, string>> = {
  zh: {
    auto: '自动阶段',
    premarket: '盘前',
    intraday: '盘中',
    postmarket: '盘后',
  },
  en: {
    auto: 'Auto',
    premarket: 'Pre-market',
    intraday: 'Intraday',
    postmarket: 'Post-market',
  },
  ja: {
    auto: '自動',
    premarket: '寄り付き前',
    intraday: 'ザラ場',
    postmarket: '引け後',
  },
};

const MARKET_PHASE_LABELS: Record<ReportLanguage, Record<MarketPhaseValue, string>> = {
  zh: {
    premarket: '盘前',
    intraday: '盘中',
    lunch_break: '午间休市',
    closing_auction: '临近收盘',
    postmarket: '盘后',
    non_trading: '非交易日',
    unknown: '阶段未知',
  },
  en: {
    premarket: 'Pre-market',
    intraday: 'Intraday',
    lunch_break: 'Lunch break',
    closing_auction: 'Near close',
    postmarket: 'Post-market',
    non_trading: 'Non-trading',
    unknown: 'Unknown phase',
  },
  ja: {
    premarket: '寄り付き前',
    intraday: 'ザラ場',
    lunch_break: '昼休み',
    closing_auction: '引け間際',
    postmarket: '引け後',
    non_trading: '非取引日',
    unknown: '局面不明',
  },
};

const TEXT = {
  zh: {
    requestPrefix: '请求阶段',
    finalPrefix: '市场阶段',
    partialBar: '日线未完成',
  },
  en: {
    requestPrefix: 'Requested phase',
    finalPrefix: 'Market phase',
    partialBar: 'Partial bar',
  },
  ja: {
    requestPrefix: 'リクエスト局面',
    finalPrefix: '市場局面',
    partialBar: '日足未確定',
  },
} as const;

export const getRequestedPhaseLabel = (
  phase?: AnalysisPhase | null,
  language?: ReportLanguage | null,
): string | null => {
  if (!phase) {
    return null;
  }

  const reportLanguage = normalizeReportLanguage(language);
  const label = REQUEST_PHASE_LABELS[reportLanguage][phase];
  if (!label) {
    return null;
  }

  return `${TEXT[reportLanguage].requestPrefix}: ${label}`;
};

export const getMarketPhaseSummaryLabel = (
  summary?: MarketPhaseSummary | null,
  language?: ReportLanguage | null,
): string | null => {
  if (!summary) {
    return null;
  }

  const reportLanguage = normalizeReportLanguage(language);
  const phaseLabel = MARKET_PHASE_LABELS[reportLanguage][summary.phase];
  if (!phaseLabel) {
    return null;
  }

  const market = (summary.market || '').trim().toUpperCase();
  const value = market ? `${market} · ${phaseLabel}` : phaseLabel;
  return `${TEXT[reportLanguage].finalPrefix}: ${value}`;
};

export const getPartialBarLabel = (language?: ReportLanguage | null): string =>
  TEXT[normalizeReportLanguage(language)].partialBar;
