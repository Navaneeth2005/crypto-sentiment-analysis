import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ── Aesthetics ───────────────────────────────────────────────────────────────
SENTIMENT_ORDER = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
PALETTE = {
    'Extreme Fear': '#d62728',
    'Fear':         '#ff7f0e',
    'Neutral':      '#7f7f7f',
    'Greed':        '#2ca02c',
    'Extreme Greed':'#1f77b4',
}
sns.set_theme(style='darkgrid', font_scale=1.1)
plt.rcParams.update({'figure.dpi': 150, 'savefig.dpi': 150,
                     'savefig.bbox': 'tight', 'font.family': 'DejaVu Sans'})

VIS = '/home/claude/crypto-sentiment-analysis/visuals'

# ═══════════════════════════════════════════════════════════════════════════
# 1. LOAD & CLEAN
# ═══════════════════════════════════════════════════════════════════════════
fg = pd.read_csv('/home/claude/crypto-sentiment-analysis/data/fear_greed.csv')
fg['date'] = pd.to_datetime(fg['date'])
fg['classification'] = pd.Categorical(fg['classification'], categories=SENTIMENT_ORDER, ordered=True)

hd = pd.read_csv('/home/claude/crypto-sentiment-analysis/data/hyperliquid.csv')
hd['date'] = pd.to_datetime(hd['Timestamp IST'], format='%d-%m-%Y %H:%M', dayfirst=True).dt.normalize()
hd['Closed PnL'] = pd.to_numeric(hd['Closed PnL'], errors='coerce')
hd['Size USD']   = pd.to_numeric(hd['Size USD'],   errors='coerce')
hd['is_win']     = hd['Closed PnL'] > 0
hd['is_loss']    = hd['Closed PnL'] < 0
hd['is_long']    = hd['Direction'].str.contains('Long|Buy', na=False)
hd['is_short']   = hd['Direction'].str.contains('Short|Sell', na=False)

# ═══════════════════════════════════════════════════════════════════════════
# 2. MERGE
# ═══════════════════════════════════════════════════════════════════════════
merged = hd.merge(fg[['date','classification','value']], on='date', how='left')
merged.dropna(subset=['classification'], inplace=True)
merged['classification'] = pd.Categorical(merged['classification'], categories=SENTIMENT_ORDER, ordered=True)

print(f"Merged dataset: {len(merged):,} trades | {merged['Account'].nunique()} accounts | "
      f"{merged['Coin'].nunique()} coins | {merged['date'].min().date()} → {merged['date'].max().date()}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. FIG 1 – SENTIMENT DISTRIBUTION & TIMELINE
# ═══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
fig.suptitle('Bitcoin Market Sentiment Overview (2018–2025)', fontsize=15, fontweight='bold')

counts = fg['classification'].value_counts().reindex(SENTIMENT_ORDER)
bars = axes[0].bar(SENTIMENT_ORDER, counts, color=[PALETTE[s] for s in SENTIMENT_ORDER], edgecolor='white', linewidth=0.8)
axes[0].set_title('Sentiment Frequency Distribution')
axes[0].set_xlabel('Sentiment State')
axes[0].set_ylabel('Number of Days')
for bar, val in zip(bars, counts):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+10, f'{val:,}', ha='center', va='bottom', fontsize=9)

# Rolling 30-day avg sentiment value
fg_sorted = fg.sort_values('date')
fg_sorted['rolling_val'] = fg_sorted['value'].rolling(30).mean()
axes[1].fill_between(fg_sorted['date'], fg_sorted['value'], alpha=0.2, color='steelblue')
axes[1].plot(fg_sorted['date'], fg_sorted['rolling_val'], color='steelblue', lw=1.5, label='30-day avg')
axes[1].axhline(25, color=PALETTE['Fear'], ls='--', lw=1, label='Fear threshold (25)')
axes[1].axhline(75, color=PALETTE['Greed'], ls='--', lw=1, label='Greed threshold (75)')
axes[1].set_title('Sentiment Value Timeline')
axes[1].set_xlabel('Date'); axes[1].set_ylabel('Fear & Greed Index')
axes[1].legend(fontsize=8)

plt.tight_layout()
plt.savefig(f'{VIS}/sentiment_distribution.png')
plt.close()
print("✓ Fig 1: sentiment_distribution.png")

# ═══════════════════════════════════════════════════════════════════════════
# 4. FIG 2 – PnL BY SENTIMENT
# ═══════════════════════════════════════════════════════════════════════════
active = merged[merged['Closed PnL'] != 0].copy()

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Trader Profitability by Market Sentiment', fontsize=14, fontweight='bold')

# Boxplot – clipped for readability
clip = active['Closed PnL'].quantile([0.05, 0.95])
clipped = active[active['Closed PnL'].between(clip[0.05], clip[0.95])]
sns.boxplot(data=clipped, x='classification', y='Closed PnL',
            order=SENTIMENT_ORDER, palette=PALETTE, ax=axes[0], linewidth=0.8)
axes[0].set_title('PnL Distribution (5th–95th pct)')
axes[0].set_xlabel(''); axes[0].set_ylabel('Closed PnL (USD)')
axes[0].tick_params(axis='x', rotation=30)

# Mean & Median PnL
pnl_agg = active.groupby('classification', observed=True)['Closed PnL'].agg(['mean','median']).reindex(SENTIMENT_ORDER)
x = np.arange(len(SENTIMENT_ORDER)); w = 0.35
axes[1].bar(x - w/2, pnl_agg['mean'],   w, label='Mean',   color='steelblue',  alpha=0.85)
axes[1].bar(x + w/2, pnl_agg['median'], w, label='Median', color='darkorange', alpha=0.85)
axes[1].set_xticks(x); axes[1].set_xticklabels(SENTIMENT_ORDER, rotation=30, ha='right')
axes[1].set_title('Mean vs Median PnL by Sentiment')
axes[1].set_ylabel('Closed PnL (USD)'); axes[1].legend()
axes[1].axhline(0, color='white', ls='--', lw=0.8)

# Win rate
wr = active.groupby('classification', observed=True).apply(
    lambda x: (x['Closed PnL'] > 0).mean() * 100).reindex(SENTIMENT_ORDER)
colors = [PALETTE[s] for s in SENTIMENT_ORDER]
axes[2].bar(SENTIMENT_ORDER, wr, color=colors, edgecolor='white', linewidth=0.8)
axes[2].axhline(50, color='white', ls='--', lw=1, label='50% baseline')
axes[2].set_title('Win Rate by Sentiment (%)')
axes[2].set_ylabel('Win Rate (%)'); axes[2].set_ylim(0, 70)
axes[2].tick_params(axis='x', rotation=30)
for i, (s, v) in enumerate(wr.items()):
    axes[2].text(i, v+0.5, f'{v:.1f}%', ha='center', va='bottom', fontsize=9)
axes[2].legend()

plt.tight_layout()
plt.savefig(f'{VIS}/pnl_by_sentiment.png')
plt.close()
print("✓ Fig 2: pnl_by_sentiment.png")

# ═══════════════════════════════════════════════════════════════════════════
# 5. FIG 3 – TRADING ACTIVITY & VOLUME
# ═══════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Trading Activity by Sentiment', fontsize=14, fontweight='bold')

# Trade count
tc = merged.groupby('classification', observed=True).size().reindex(SENTIMENT_ORDER)
axes[0].bar(SENTIMENT_ORDER, tc, color=[PALETTE[s] for s in SENTIMENT_ORDER], edgecolor='white')
axes[0].set_title('Number of Trades'); axes[0].set_ylabel('Trade Count')
axes[0].tick_params(axis='x', rotation=30)
for i, v in enumerate(tc): axes[0].text(i, v+200, f'{v:,}', ha='center', va='bottom', fontsize=8)

# Volume
vol = merged.groupby('classification', observed=True)['Size USD'].sum().reindex(SENTIMENT_ORDER) / 1e6
axes[1].bar(SENTIMENT_ORDER, vol, color=[PALETTE[s] for s in SENTIMENT_ORDER], edgecolor='white')
axes[1].set_title('Total Trading Volume'); axes[1].set_ylabel('Volume (USD Millions)')
axes[1].tick_params(axis='x', rotation=30)
for i, v in enumerate(vol): axes[1].text(i, v+0.5, f'${v:.1f}M', ha='center', va='bottom', fontsize=8)

# Long vs Short ratio
ls = merged.groupby('classification', observed=True).apply(
    lambda x: pd.Series({'Long %': x['is_long'].mean()*100, 'Short %': x['is_short'].mean()*100})
).reindex(SENTIMENT_ORDER)
x = np.arange(len(SENTIMENT_ORDER)); w = 0.35
axes[2].bar(x - w/2, ls['Long %'],  w, label='Long',  color='#2ca02c', alpha=0.85)
axes[2].bar(x + w/2, ls['Short %'], w, label='Short', color='#d62728', alpha=0.85)
axes[2].set_xticks(x); axes[2].set_xticklabels(SENTIMENT_ORDER, rotation=30, ha='right')
axes[2].set_title('Long vs Short by Sentiment'); axes[2].set_ylabel('%'); axes[2].legend()

plt.tight_layout()
plt.savefig(f'{VIS}/trading_activity.png')
plt.close()
print("✓ Fig 3: trading_activity.png")

# ═══════════════════════════════════════════════════════════════════════════
# 6. FIG 4 – LEVERAGE ANALYSIS (using Size USD / Size Tokens as proxy)
# ═══════════════════════════════════════════════════════════════════════════
merged['notional_ratio'] = (merged['Size USD'] / merged['Size Tokens']).replace([np.inf, -np.inf], np.nan)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Position Size & Volume by Sentiment', fontsize=14, fontweight='bold')

sns.violinplot(data=merged[merged['Size USD'] < merged['Size USD'].quantile(0.95)],
               x='classification', y='Size USD', order=SENTIMENT_ORDER,
               palette=PALETTE, ax=axes[0], linewidth=0.6)
axes[0].set_title('Position Size Distribution (USD)')
axes[0].set_xlabel(''); axes[0].set_ylabel('Size (USD)')
axes[0].tick_params(axis='x', rotation=30)

avg_size = merged.groupby('classification', observed=True)['Size USD'].mean().reindex(SENTIMENT_ORDER)
axes[1].bar(SENTIMENT_ORDER, avg_size, color=[PALETTE[s] for s in SENTIMENT_ORDER], edgecolor='white')
axes[1].set_title('Average Position Size (USD)'); axes[1].set_ylabel('Avg Size (USD)')
axes[1].tick_params(axis='x', rotation=30)
for i, v in enumerate(avg_size): axes[1].text(i, v+100, f'${v:,.0f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig(f'{VIS}/leverage_analysis.png')
plt.close()
print("✓ Fig 4: leverage_analysis.png")

# ═══════════════════════════════════════════════════════════════════════════
# 7. FIG 5 – CORRELATION HEATMAP
# ═══════════════════════════════════════════════════════════════════════════
sentiment_num = {'Extreme Fear':1,'Fear':2,'Neutral':3,'Greed':4,'Extreme Greed':5}
merged['sentiment_num'] = merged['classification'].map(sentiment_num)

corr_df = merged[['sentiment_num','Closed PnL','Size USD','Size Tokens','Fee','is_win','is_long','is_short']].copy()
corr_df.columns = ['Sentiment','Closed PnL','Size USD','Size Tokens','Fee','Is Win','Is Long','Is Short']
corr_matrix = corr_df.corr()

fig, ax = plt.subplots(figsize=(9, 7))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, linewidths=0.5, ax=ax, cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Matrix: Sentiment & Trading Variables', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(f'{VIS}/correlation_heatmap.png')
plt.close()
print("✓ Fig 5: correlation_heatmap.png")

# ═══════════════════════════════════════════════════════════════════════════
# 8. FIG 6 – TOP TRADERS & PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════
top20 = (merged.groupby('Account')['Closed PnL']
         .sum().sort_values(ascending=False).head(20))
top20_short = [a[:8]+'…' for a in top20.index]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Account-Level Performance Analysis', fontsize=14, fontweight='bold')

colors_bar = ['#2ca02c' if v >= 0 else '#d62728' for v in top20.values]
axes[0].barh(top20_short[::-1], top20.values[::-1], color=colors_bar[::-1], edgecolor='white')
axes[0].set_title('Top 20 Traders by Total PnL')
axes[0].set_xlabel('Total Closed PnL (USD)')
axes[0].axvline(0, color='white', lw=0.8)

# Best traders in Fear vs Greed
fear_pnl = merged[merged['classification'].isin(['Fear','Extreme Fear'])].groupby('Account')['Closed PnL'].sum()
greed_pnl = merged[merged['classification'].isin(['Greed','Extreme Greed'])].groupby('Account')['Closed PnL'].sum()
compare = pd.DataFrame({'Fear/Ext.Fear PnL': fear_pnl, 'Greed/Ext.Greed PnL': greed_pnl}).dropna()
compare['addr'] = [a[:8]+'…' for a in compare.index]
compare_top = compare.nlargest(10, 'Fear/Ext.Fear PnL')
x = np.arange(len(compare_top)); w = 0.35
axes[1].bar(x - w/2, compare_top['Fear/Ext.Fear PnL'],  w, label='Fear Periods',  color='#ff7f0e', alpha=0.85)
axes[1].bar(x + w/2, compare_top['Greed/Ext.Greed PnL'], w, label='Greed Periods', color='#1f77b4', alpha=0.85)
axes[1].set_xticks(x); axes[1].set_xticklabels(compare_top['addr'], rotation=45, ha='right', fontsize=7)
axes[1].set_title('Top 10 Traders: Fear vs Greed PnL')
axes[1].set_ylabel('Total PnL (USD)'); axes[1].legend()
axes[1].axhline(0, color='white', ls='--', lw=0.8)

plt.tight_layout()
plt.savefig(f'{VIS}/trader_performance.png')
plt.close()
print("✓ Fig 6: trader_performance.png")

# ═══════════════════════════════════════════════════════════════════════════
# 9. FIG 7 – TOP COINS BY SENTIMENT
# ═══════════════════════════════════════════════════════════════════════════
top_coins = merged['Coin'].value_counts().head(8).index.tolist()
coin_sent = (merged[merged['Coin'].isin(top_coins)]
             .groupby(['Coin','classification'], observed=True)
             .size().unstack(fill_value=0)
             .reindex(columns=SENTIMENT_ORDER))

fig, ax = plt.subplots(figsize=(12, 5))
coin_sent.plot(kind='bar', stacked=True, ax=ax,
               color=[PALETTE[s] for s in SENTIMENT_ORDER], edgecolor='white', linewidth=0.4)
ax.set_title('Top 8 Coins — Trade Count by Sentiment', fontsize=13, fontweight='bold')
ax.set_xlabel('Coin'); ax.set_ylabel('Number of Trades')
ax.legend(title='Sentiment', bbox_to_anchor=(1.01, 1), loc='upper left')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig(f'{VIS}/coin_sentiment.png')
plt.close()
print("✓ Fig 7: coin_sentiment.png")

# ═══════════════════════════════════════════════════════════════════════════
# 10. STATISTICAL ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
groups = [active[active['classification']==s]['Closed PnL'].dropna() for s in SENTIMENT_ORDER]
f_stat, p_anova = stats.f_oneway(*groups)

# Pearson correlation: sentiment_num vs Closed PnL
r, p_pearson = stats.pearsonr(
    merged.dropna(subset=['sentiment_num','Closed PnL'])['sentiment_num'],
    merged.dropna(subset=['sentiment_num','Closed PnL'])['Closed PnL']
)

# t-test: Fear vs Greed PnL
fear_pnl_vals  = active[active['classification'].isin(['Fear','Extreme Fear'])]['Closed PnL']
greed_pnl_vals = active[active['classification'].isin(['Greed','Extreme Greed'])]['Closed PnL']
t_stat, p_ttest = stats.ttest_ind(fear_pnl_vals, greed_pnl_vals, equal_var=False)

print("\n══ STATISTICAL RESULTS ══")
print(f"ANOVA across all sentiment groups: F={f_stat:.3f}, p={p_anova:.4f} {'**SIGNIFICANT**' if p_anova<0.05 else ''}")
print(f"Pearson r (sentiment vs PnL): r={r:.4f}, p={p_pearson:.4f}")
print(f"Welch t-test (Fear vs Greed PnL): t={t_stat:.3f}, p={p_ttest:.4f} {'**SIGNIFICANT**' if p_ttest<0.05 else ''}")

# ═══════════════════════════════════════════════════════════════════════════
# 11. SUMMARY STATS (returned for report)
# ═══════════════════════════════════════════════════════════════════════════
summary = active.groupby('classification', observed=True)['Closed PnL'].agg(
    trades='count', mean_pnl='mean', median_pnl='median',
    total_pnl='sum', std_pnl='std'
).reindex(SENTIMENT_ORDER)
summary['win_rate'] = active.groupby('classification', observed=True).apply(
    lambda x: (x['Closed PnL']>0).mean()*100).reindex(SENTIMENT_ORDER)
summary['sharpe_proxy'] = summary['mean_pnl'] / summary['std_pnl']

print("\n══ PnL SUMMARY BY SENTIMENT ══")
print(summary.round(3).to_string())

vol_summary = merged.groupby('classification', observed=True)['Size USD'].agg(['mean','sum']).reindex(SENTIMENT_ORDER)
vol_summary.columns = ['avg_size_usd', 'total_volume_usd']
print("\n══ VOLUME SUMMARY BY SENTIMENT ══")
print(vol_summary.round(0).to_string())

# Save key numbers for report
results = dict(
    f_stat=f_stat, p_anova=p_anova, r_pearson=r, p_pearson=p_pearson,
    t_stat=t_stat, p_ttest=p_ttest,
    summary=summary, vol_summary=vol_summary,
    total_trades=len(merged), n_accounts=merged['Account'].nunique(),
    date_range=(merged['date'].min().date(), merged['date'].max().date()),
    total_pnl=active['Closed PnL'].sum(),
    top20=top20
)
print("\n✅ All analysis complete.")
