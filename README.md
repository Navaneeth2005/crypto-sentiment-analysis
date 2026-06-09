# 📊 Bitcoin Sentiment × Hyperliquid Trader Analysis

> A quantitative study of how Bitcoin market sentiment influences trader behavior and profitability on the Hyperliquid DEX.

---

## 🗂️ Project Structure

```
crypto-sentiment-analysis/
├── data/
│   ├── fear_greed.csv          # Bitcoin Fear & Greed Index (2018–2025)
│   └── hyperliquid.csv         # Hyperliquid on-chain trade history
├── notebooks/
│   └── analysis.ipynb          # End-to-end analysis notebook
├── visuals/
│   ├── sentiment_distribution.png
│   ├── pnl_by_sentiment.png
│   ├── trading_activity.png
│   ├── leverage_analysis.png
│   ├── correlation_heatmap.png
│   ├── trader_performance.png
│   └── coin_sentiment.png
├── report/
│   └── final_report.md
├── README.md
└── requirements.txt
```

---

## 🎯 Objective

Analyze whether Bitcoin market sentiment (Fear & Greed Index) meaningfully predicts or explains trader behavior and profitability on Hyperliquid, a decentralized perpetuals exchange.

---

## 📦 Datasets

| Dataset | Source | Records | Period |
|---------|--------|---------|--------|
| Fear & Greed Index | Alternative.me | 2,644 days | Feb 2018 – May 2025 |
| Hyperliquid Trades | Hyperliquid DEX | 211,224 trades | May 2023 – May 2025 |

---

## 🔬 Methodology

1. **Data Cleaning** — Parse timestamps, handle missing values, encode sentiment categories
2. **Merge** — Left-join trades to daily sentiment on `date`
3. **EDA** — Profitability, volume, long/short ratios, top coins per sentiment
4. **Statistics** — One-way ANOVA, Pearson correlation, Welch t-test
5. **Feature Engineering** — Trade efficiency, daily PnL, sentiment transitions

---

## 🔑 Key Findings

- **Extreme Greed** yields the highest mean PnL ($130) and win rate (89%)
- **Fear** periods see the largest average position sizes ($7,816) and highest total volume ($483M)
- **ANOVA test is statistically significant** (F=7.74, p<0.0001) — sentiment does influence PnL distributions
- **Fear vs Greed t-test is NOT significant** (p=0.69) — mean PnL levels are statistically similar between these two states; the difference lies in variance and win rates
- HYPE, BTC, ETH, and SOL are the top traded assets across all sentiment states

---

## 💡 Trading Recommendations

| Recommendation | Rationale |
|---------------|-----------|
| Scale up during Extreme Greed | 89% win rate, highest mean PnL |
| Reduce position size during Fear | Largest positions taken, highest PnL variance |
| Stay active during Extreme Fear | Still produces positive mean PnL |
| Use sentiment as a signal overlay | Significant but weak predictor (r=0.006) |

---

## 🚀 Installation

```bash
git clone https://github.com/yourusername/crypto-sentiment-analysis
cd crypto-sentiment-analysis
pip install -r requirements.txt
jupyter notebook notebooks/analysis.ipynb
```

---

## 📄 Resume-Worthy Description

> **Crypto Sentiment × Trading Behavior Analysis** | Python, Pandas, Seaborn, SciPy
> 
> Built an end-to-end quantitative analysis pipeline integrating 211K+ on-chain perpetuals trades from Hyperliquid DEX with the Bitcoin Fear & Greed Index (2,644 days). Engineered features including trade efficiency ratios, daily account-level PnL, and sentiment transition matrices. Applied one-way ANOVA, Pearson correlation, and Welch t-tests to identify statistically significant relationships between market sentiment and trader profitability. Produced 7 publication-quality visualizations revealing that Extreme Greed periods yield 89% win rates vs 76% in Extreme Fear, while Fear periods paradoxically attract the largest position sizes.

---

## 📚 References

- [Alternative.me Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/)
- [Hyperliquid DEX](https://hyperliquid.xyz/)
