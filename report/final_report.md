# 📑 Final Report: Bitcoin Sentiment × Hyperliquid Trader Analysis

---

## Executive Summary

This analysis examined 211,224 on-chain trades by 32 Hyperliquid accounts across 246 assets between May 2023 and May 2025, merged with the daily Bitcoin Fear & Greed Index. The central question — **does market sentiment materially influence trader behavior and profitability?** — is answered: **yes, but the relationship is more nuanced than directionally obvious.**

Statistically, sentiment groups produce significantly different PnL distributions (ANOVA F=7.74, p<0.0001). However, the raw correlation between sentiment score and individual trade PnL is very weak (r=0.006), meaning sentiment explains a small portion of variance at the trade level but becomes visible in aggregate patterns.

---

## Dataset Overview

| Parameter | Value |
|-----------|-------|
| Total Trades | 211,224 |
| Accounts | 32 |
| Coins Traded | 246 |
| Period | May 2023 – May 2025 |
| Sentiment Data | Feb 2018 – May 2025 (2,644 days) |
| Total Matched Trades | 211,218 (99.997% match rate) |

---

## Key Findings

### 1. Profitability by Sentiment

| Sentiment | Trades | Mean PnL | Median PnL | Win Rate | Sharpe Proxy |
|-----------|--------|----------|------------|----------|--------------|
| Extreme Fear | 10,406 | $71.03 | $6.39 | 76.2% | 0.044 |
| Fear | 29,808 | $112.63 | $6.35 | 87.3% | 0.084 |
| Neutral | 18,159 | $71.20 | $4.58 | 82.4% | 0.096 |
| Greed | 25,176 | $85.40 | $4.93 | 76.9% | 0.054 |
| Extreme Greed | 20,853 | **$130.21** | **$8.53** | **89.2%** | **0.123** |

**Finding:** Extreme Greed is the best environment for profitable trading by every metric. Extreme Fear is not the disaster many expect — it still generates positive mean PnL but with wider variance.

### 2. Volume & Position Sizing

| Sentiment | Avg Position (USD) | Total Volume |
|-----------|--------------------|--------------|
| Extreme Fear | $5,350 | $114M |
| **Fear** | **$7,816** | **$483M** |
| Neutral | $4,783 | $180M |
| Greed | $5,737 | $289M |
| Extreme Greed | $3,112 | $124M |

**Finding:** Fear periods attract the most capital and the largest average position sizes — a contrarian signal. Traders are most aggressive exactly when sentiment is most negative.

### 3. Long vs Short Behavior

Across all sentiment states, long trades slightly outnumber short trades (~51% long vs ~49% short), indicating these accounts maintain a mild long bias regardless of sentiment regime.

### 4. Top Assets

HYPE (Hyperliquid's native token) dominates at 68,005 trades (~32% of all trades), followed by a vault token (@107), BTC, ETH, and SOL. The concentration in HYPE reflects the platform-native incentives of these accounts.

---

## Statistical Findings

| Test | Statistic | p-value | Interpretation |
|------|-----------|---------|----------------|
| One-Way ANOVA | F = 7.738 | < 0.0001 | ✅ Sentiment significantly differentiates PnL distributions |
| Pearson r (Sentiment → PnL) | r = 0.006 | 0.0061 | ✅ Significant but very weak linear relationship |
| Welch t-test (Fear vs Greed) | t = -0.403 | 0.687 | ❌ Mean PnL between Fear and Greed is NOT statistically different |

**Interpretation:** Sentiment creates structural differences across all five groups (ANOVA), but the simple Fear vs Greed binary is insufficient — the important distinction is **Extreme** states, particularly Extreme Greed.

---

## Trading Recommendations

### Risk Management
- Tighten stop-losses during Fear periods where position sizes tend to balloon
- Use sentiment as a volatility proxy — fear periods see higher PnL variance

### Position Sizing
- Scale up cautiously during Extreme Greed (best win rates and returns)
- Reduce position sizes during Fear despite temptation — volume is highest but so is variance

### Sentiment-Aware Strategies
- **Fear → contrarian opportunity**: High volume with positive mean PnL; experienced traders can profit
- **Extreme Greed → trend-following**: 89% win rate suggests momentum trading works best here
- **Extreme Fear → selective hedging**: Lowest average win rate; prefer conservative sizing

### Leverage & Efficiency
- Trade efficiency (PnL per USD) is highest during Neutral and Extreme Greed periods
- Avoid over-leveraging during Fear — the data shows capital concentration without proportional returns

---

## Final Conclusion

**"How does Bitcoin market sentiment influence trader behavior and profitability?"**

Bitcoin market sentiment measurably influences both how traders behave and how they perform, but not always in the expected direction:

1. **Greed → Better performance**: Extreme Greed produces the highest win rates and mean PnL, confirming that momentum/trend conditions reward active traders.

2. **Fear → More capital, not less**: Contrary to "buy fear" intuition, Fear periods attract the most trading volume and largest positions, suggesting many traders are trying to catch bottoms rather than sitting on the sidelines.

3. **Sentiment is a statistically significant but practically weak predictor**: At the individual trade level, sentiment explains very little variance. Its value is as a regime filter — distinguishing structural risk environments — rather than a trade-by-trade signal.

4. **Extreme states matter more than the Fear/Greed binary**: The ANOVA is significant but the Fear vs Greed t-test is not. The real differentiator is Extreme Greed (best) vs Extreme Fear (most volatile).

