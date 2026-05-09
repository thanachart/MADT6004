"""Build Module 2 notebook: batch SKU × Branch forecasting."""
import sys
sys.path.insert(0, ".")
from _nbutil import cell, write_notebook

cells = [
    cell("md", """# Module 2 — Batch Forecasting (SKU × Branch)
**MADT6004 Wrap-Up · Brew Lab BKK case**

Khun Ploy: *"Stop telling me about the past. How much will each SKU sell at each branch over the next 30 days?"*

What you'll do:
1. Build a daily-level **SKU × Branch** demand panel.
2. Loop a **batch forecast** across many series (top 5 SKUs × 12 branches = 60 series).
3. Compare three methods: **Naive**, **Seasonal Naive (weekly)**, **Holt-Winters**.
4. Evaluate with **RMSE** on a holdout window.
5. Pick the winning method per series and produce 30-day forecasts."""),

    cell("md", "## 1. Setup"),

    cell("code", """import sqlite3
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
warnings.filterwarnings("ignore")
plt.rcParams["figure.dpi"] = 100

conn = sqlite3.connect("../data/brewlab.db")
print("Loaded.")"""),

    cell("md", "## 2. Build daily SKU × Branch panel"),

    cell("code", """daily = pd.read_sql('''
SELECT date(t.datetime)  AS d,
       t.branch_id,
       oi.product_id,
       SUM(oi.qty)        AS units
FROM transactions t
JOIN order_items oi ON t.order_id = oi.order_id
GROUP BY date(t.datetime), t.branch_id, oi.product_id
''', conn)
daily['d'] = pd.to_datetime(daily['d'])

products = pd.read_sql("SELECT product_id, name AS product, category FROM products", conn)
branches = pd.read_sql("SELECT branch_id, name AS branch FROM branches", conn)
daily = daily.merge(products, on='product_id').merge(branches, on='branch_id')

# Pick top 5 SKUs by total units
top_skus = (daily.groupby(['product_id','product'])['units'].sum()
            .sort_values(ascending=False).head(5).reset_index())
print("Top 5 SKUs:")
print(top_skus)

target_skus = top_skus['product_id'].tolist()
target_branches = branches['branch_id'].tolist()
print(f"\\nTotal series to forecast: {len(target_skus)} SKUs × {len(target_branches)} branches = {len(target_skus)*len(target_branches)}")"""),

    cell("md", """## 3. Define forecasting functions

Three baseline methods:
- **Naive** — predict the last value forever
- **Seasonal Naive** — predict the same day-of-week from last week
- **Holt-Winters** — exponential smoothing with trend + weekly seasonality"""),

    cell("code", """def make_series(daily, sku, branch):
    \"\"\"Return a daily series, zero-filled for missing days.\"\"\"
    sub = daily[(daily.product_id == sku) & (daily.branch_id == branch)][['d', 'units']]
    if len(sub) == 0:
        return None
    sub = sub.set_index('d').sort_index()
    full_idx = pd.date_range(sub.index.min(), sub.index.max(), freq='D')
    sub = sub.reindex(full_idx, fill_value=0)
    sub.index.name = 'd'
    return sub['units']

def forecast_naive(train, h):
    return np.repeat(train.iloc[-1], h)

def forecast_seasonal_naive(train, h, season=7):
    last_season = train.iloc[-season:].values
    return np.tile(last_season, int(np.ceil(h / season)))[:h]

def forecast_holt_winters(train, h):
    if len(train) < 21:
        return forecast_seasonal_naive(train, h)
    try:
        m = ExponentialSmoothing(train, seasonal_periods=7,
                                  trend="add", seasonal="add",
                                  initialization_method="estimated").fit()
        return m.forecast(h).values
    except Exception:
        return forecast_seasonal_naive(train, h)

def rmse(y_true, y_pred):
    return float(np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2)))"""),

    cell("md", "## 4. Batch loop — forecast all series + collect RMSE"),

    cell("code", """HOLDOUT_DAYS = 14

records = []
for sku in target_skus:
    for br in target_branches:
        s = make_series(daily, sku, br)
        if s is None or len(s) < 60:
            continue
        train = s.iloc[:-HOLDOUT_DAYS]
        test  = s.iloc[-HOLDOUT_DAYS:]

        preds = {
            "naive":          forecast_naive(train, HOLDOUT_DAYS),
            "seasonal_naive": forecast_seasonal_naive(train, HOLDOUT_DAYS),
            "holt_winters":   forecast_holt_winters(train, HOLDOUT_DAYS),
        }
        for method, p in preds.items():
            records.append({
                "sku_id": sku, "branch_id": br, "method": method,
                "rmse": rmse(test.values, p),
                "test_mean": float(test.mean()),
                "n_train": len(train),
            })

eval_df = pd.DataFrame(records)
eval_df = eval_df.merge(products[['product_id','product']], left_on='sku_id', right_on='product_id', how='left') \\
                 .merge(branches, on='branch_id', how='left')
print(f"Evaluated {eval_df.groupby(['sku_id','branch_id']).ngroups} series × 3 methods.")
eval_df.head()"""),

    cell("md", "## 5. Method comparison — which baseline wins overall?"),

    cell("code", """summary = eval_df.groupby('method').agg(
    mean_rmse=('rmse','mean'),
    median_rmse=('rmse','median'),
    n=('rmse','count')
).sort_values('mean_rmse')
print(summary)

# Pick winner per series
wins = (eval_df.sort_values('rmse')
              .groupby(['sku_id','branch_id']).head(1)
              .groupby('method').size().reset_index(name='wins'))
print("\\nWins per method (lowest RMSE on each series):")
print(wins.sort_values('wins', ascending=False))"""),

    cell("md", "## 6. Visualize — RMSE distribution by method"),

    cell("code", """fig, axes = plt.subplots(1, 2, figsize=(13, 4))
eval_df.boxplot(column='rmse', by='method', ax=axes[0])
axes[0].set_title("RMSE by Method")
axes[0].set_ylabel("RMSE (units / day)")
axes[0].set_xlabel("")
plt.suptitle("")

# Heatmap: best method's RMSE by SKU × Branch
best = eval_df.sort_values('rmse').groupby(['sku_id','branch_id']).head(1)
pv = best.pivot(index='product', columns='branch', values='rmse')
import seaborn as sns
sns.heatmap(pv, annot=True, fmt=".1f", cmap="Reds", ax=axes[1], cbar_kws={'label':'RMSE'})
axes[1].set_title("Best-method RMSE: SKU × Branch")
plt.tight_layout()
plt.show()"""),

    cell("md", "## 7. Generate the 30-day forecast for each series"),

    cell("code", """FORECAST_HORIZON = 30
final = []
for sku in target_skus:
    for br in target_branches:
        s = make_series(daily, sku, br)
        if s is None or len(s) < 60:
            continue
        # Pick winning method on holdout
        sub = eval_df[(eval_df.sku_id == sku) & (eval_df.branch_id == br)].sort_values('rmse')
        if sub.empty:
            continue
        best_method = sub.iloc[0]['method']
        if best_method == "naive":
            fc = forecast_naive(s, FORECAST_HORIZON)
        elif best_method == "seasonal_naive":
            fc = forecast_seasonal_naive(s, FORECAST_HORIZON)
        else:
            fc = forecast_holt_winters(s, FORECAST_HORIZON)
        future_dates = pd.date_range(s.index.max() + pd.Timedelta(days=1), periods=FORECAST_HORIZON, freq='D')
        for d, v in zip(future_dates, fc):
            final.append({"sku_id": sku, "branch_id": br, "date": d, "forecast": max(0, float(v)),
                          "method": best_method})

forecast_df = pd.DataFrame(final)
forecast_df = forecast_df.merge(products[['product_id','product']], left_on='sku_id', right_on='product_id') \\
                          .merge(branches, on='branch_id')
print(f"30-day forecasts: {len(forecast_df)} rows ({forecast_df.groupby(['sku_id','branch_id']).ngroups} series)")
forecast_df.head()"""),

    cell("md", "## 8. Visualize one example — train + holdout + forecast"),

    cell("code", """example_sku = target_skus[0]
example_branch = 1  # Asoke
s = make_series(daily, example_sku, example_branch)
fc = forecast_df[(forecast_df.sku_id == example_sku) & (forecast_df.branch_id == example_branch)]

fig, ax = plt.subplots(figsize=(13, 4))
ax.plot(s.index, s.values, label="Actual", color="#1F2937", lw=0.8)
ax.plot(fc['date'], fc['forecast'], label=f"30-day forecast ({fc['method'].iloc[0]})", color="#0891B2", lw=2)
ax.axvspan(s.index.max() - pd.Timedelta(days=14), s.index.max(), alpha=0.1, color="#D97706", label="Holdout window")
prod = products[products.product_id == example_sku]['product'].iloc[0]
br_name = branches[branches.branch_id == example_branch]['branch'].iloc[0]
ax.set_title(f"{prod} @ {br_name} — daily units + 30d forecast", fontsize=12)
ax.set_ylabel("Units / day")
ax.legend()
plt.tight_layout()
plt.show()"""),

    cell("md", """## 9. Discussion prompts

1. Why does **seasonal naive** often beat fancier methods? When does **Holt-Winters** earn its keep?
2. Look at the heatmap — are some branches systematically harder to forecast? Why might that be?
3. RMSE penalizes large errors heavily. Would **MAPE** or **MAE** change which method wins?
4. **Operational use:** how would you use these forecasts? Inventory? Staffing? Roasting schedule?

**Next:** Module 3 — predicting who responds to the comeback campaign, with imbalanced classes."""),
]

write_notebook("02_batch_forecasting_sku_branch.ipynb", cells)
print("Module 2 notebook written.")
