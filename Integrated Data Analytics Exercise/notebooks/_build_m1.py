"""Build Module 1 notebook: causal-chain hypothesis sweep."""
import sys
sys.path.insert(0, ".")
from _nbutil import cell, write_notebook

cells = [
    cell("md", """# Module 1 — Causal-Chain Hypothesis Sweep
**MADT6004 Wrap-Up · Brew Lab BKK case**

Khun Ploy: *"Revenue is lumpy across branches and weeks. Tell me what's actually true and what we just assumed."*

What you'll do:
1. Identify a **causal chain** as a Python dictionary — every relationship we want to test, with cause, effect, and data types.
2. Write a **dispatch function** that picks the right test (t-test / ANOVA / Pearson / chi-square) based on the data types in each chain.
3. Run the **sweep** across all chains, apply **FDR correction** (Benjamini-Hochberg), and filter to significant findings.
4. Build a **dashboard** of significant relationships."""),

    cell("md", "## 1. Setup"),

    cell("code", """import sqlite3
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.multitest import multipletests
import statsmodels.formula.api as smf
import warnings
warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 100

DB_PATH = "../data/brewlab.db"
conn = sqlite3.connect(DB_PATH)
print("Tables:", [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()])"""),

    cell("md", "## 2. Build the analysis frame — daily branch panel"),

    cell("code", """# Aggregate transactions to daily-branch level + join branch attributes
panel = pd.read_sql('''
SELECT date(t.datetime) AS d,
       t.branch_id,
       b.name      AS branch_name,
       b.district,
       b.has_drive_thru,
       b.seats,
       b.size_sqm,
       b.base_traffic,
       SUM(t.total)        AS revenue,
       COUNT(*)            AS orders,
       AVG(t.total)        AS avg_ticket,
       SUM(CASE WHEN t.channel='app' THEN 1 ELSE 0 END)*1.0 / COUNT(*) AS app_share,
       MAX(CASE WHEN t.promo_id IS NOT NULL THEN 1 ELSE 0 END) AS promo_active
FROM transactions t
JOIN branches b ON t.branch_id = b.branch_id
GROUP BY date(t.datetime), t.branch_id
''', conn)
panel['d'] = pd.to_datetime(panel['d'])
panel['is_weekend'] = (panel['d'].dt.weekday >= 5).astype(int)
panel['month']      = panel['d'].dt.to_period('M').astype(str)
panel.head()"""),

    cell("md", """## 3. Define the causal chain as a dictionary

Each entry is a *hypothesized relationship*. We declare:
- `cause` — the explanatory variable
- `effect` — the outcome variable
- `cause_type` / `effect_type` — `binary`, `categorical`, `continuous`
- `subset` — optional filter (e.g., only weekends)
- `direction` — what we expect (for interpretation, not testing)

This dictionary is the *audit trail* of what was tested. No more "I ran 50 tests and reported the p<.05 ones."
"""),

    cell("code", """CAUSAL_CHAIN = {
    "h01_dt_revenue":        {"cause":"has_drive_thru", "effect":"revenue",     "cause_type":"binary",      "effect_type":"continuous"},
    "h02_dt_weekend_revenue":{"cause":"has_drive_thru", "effect":"revenue",     "cause_type":"binary",      "effect_type":"continuous", "subset":"is_weekend==1"},
    "h03_dt_weekday_revenue":{"cause":"has_drive_thru", "effect":"revenue",     "cause_type":"binary",      "effect_type":"continuous", "subset":"is_weekend==0"},
    "h04_weekend_revenue":   {"cause":"is_weekend",     "effect":"revenue",     "cause_type":"binary",      "effect_type":"continuous"},
    "h05_promo_revenue":     {"cause":"promo_active",   "effect":"revenue",     "cause_type":"binary",      "effect_type":"continuous"},
    "h06_promo_orders":      {"cause":"promo_active",   "effect":"orders",      "cause_type":"binary",      "effect_type":"continuous"},
    "h07_seats_revenue":     {"cause":"seats",          "effect":"revenue",     "cause_type":"continuous",  "effect_type":"continuous"},
    "h08_size_revenue":      {"cause":"size_sqm",       "effect":"revenue",     "cause_type":"continuous",  "effect_type":"continuous"},
    "h09_seats_orders":      {"cause":"seats",          "effect":"orders",      "cause_type":"continuous",  "effect_type":"continuous"},
    "h10_appshare_ticket":   {"cause":"app_share",      "effect":"avg_ticket",  "cause_type":"continuous",  "effect_type":"continuous"},
    "h11_district_revenue":  {"cause":"district",       "effect":"revenue",     "cause_type":"categorical", "effect_type":"continuous"},
    "h12_district_ticket":   {"cause":"district",       "effect":"avg_ticket",  "cause_type":"categorical", "effect_type":"continuous"},
    "h13_dt_avg_ticket":     {"cause":"has_drive_thru", "effect":"avg_ticket",  "cause_type":"binary",      "effect_type":"continuous"},
    "h14_dt_appshare":       {"cause":"has_drive_thru", "effect":"app_share",   "cause_type":"binary",      "effect_type":"continuous"},
    "h15_weekend_ticket":    {"cause":"is_weekend",     "effect":"avg_ticket",  "cause_type":"binary",      "effect_type":"continuous"},
    "h16_promo_ticket":      {"cause":"promo_active",   "effect":"avg_ticket",  "cause_type":"binary",      "effect_type":"continuous"},
    "h17_traffic_revenue":   {"cause":"base_traffic",   "effect":"revenue",     "cause_type":"continuous",  "effect_type":"continuous"},
    "h18_dt_orders_wknd":    {"cause":"has_drive_thru", "effect":"orders",      "cause_type":"binary",      "effect_type":"continuous", "subset":"is_weekend==1"},
    "h19_size_orders":       {"cause":"size_sqm",       "effect":"orders",      "cause_type":"continuous",  "effect_type":"continuous"},
    "h20_appshare_orders":   {"cause":"app_share",      "effect":"orders",      "cause_type":"continuous",  "effect_type":"continuous"},
}
print(f"{len(CAUSAL_CHAIN)} hypotheses queued.")"""),

    cell("md", """## 4. Dispatch function — pick the right test by data types

| Cause | Effect | Test |
|---|---|---|
| binary | continuous | Welch's t-test |
| categorical (k>2) | continuous | One-way ANOVA |
| continuous | continuous | Pearson correlation |
| categorical | categorical | Chi-square |

The function returns a uniform schema (statistic, p-value, effect-size proxy, direction)."""),

    cell("code", """def run_test(df, h):
    cause, effect = h["cause"], h["effect"]
    ct, et = h["cause_type"], h["effect_type"]
    if "subset" in h:
        df = df.query(h["subset"])

    if ct == "binary" and et == "continuous":
        a = df[df[cause] == 1][effect].dropna()
        b = df[df[cause] == 0][effect].dropna()
        t, p = stats.ttest_ind(a, b, equal_var=False)
        # Cohen's d
        pooled_sd = np.sqrt(((len(a)-1)*a.var() + (len(b)-1)*b.var()) / (len(a)+len(b)-2))
        d = (a.mean() - b.mean()) / pooled_sd if pooled_sd > 0 else 0
        return {"test":"t-test", "stat":t, "p":p, "effect":d,
                "summary":f"{a.mean():.0f} vs {b.mean():.0f} (n={len(a)},{len(b)})"}

    if ct == "categorical" and et == "continuous":
        groups = [g[effect].dropna().values for _, g in df.groupby(cause)]
        f, p = stats.f_oneway(*groups)
        # eta^2
        all_y = df[effect].dropna()
        ss_total = ((all_y - all_y.mean())**2).sum()
        ss_between = sum(len(g) * (g.mean() - all_y.mean())**2 for g in groups)
        eta2 = ss_between / ss_total if ss_total > 0 else 0
        return {"test":"ANOVA", "stat":f, "p":p, "effect":eta2,
                "summary":f"{len(groups)} groups, eta²={eta2:.3f}"}

    if ct == "continuous" and et == "continuous":
        sub = df[[cause, effect]].dropna()
        r, p = stats.pearsonr(sub[cause], sub[effect])
        return {"test":"Pearson", "stat":r, "p":p, "effect":r,
                "summary":f"r={r:+.3f} (n={len(sub)})"}

    if ct == "categorical" and et == "categorical":
        ct_table = pd.crosstab(df[cause], df[effect])
        chi2, p, _, _ = stats.chi2_contingency(ct_table)
        n = ct_table.values.sum()
        cramers_v = np.sqrt(chi2 / (n * (min(ct_table.shape) - 1)))
        return {"test":"chi2", "stat":chi2, "p":p, "effect":cramers_v,
                "summary":f"V={cramers_v:.3f}"}

    raise ValueError(f"Unsupported types: {ct} -> {et}")"""),

    cell("md", "## 5. Sweep all hypotheses + FDR correction"),

    cell("code", """results = []
for hid, h in CAUSAL_CHAIN.items():
    try:
        r = run_test(panel, h)
        results.append({"hypothesis": hid, "cause": h["cause"], "effect": h["effect"],
                        **r})
    except Exception as e:
        print(f"  [skip] {hid}: {e}")

res_df = pd.DataFrame(results)
# Benjamini-Hochberg FDR correction
rejected, p_adj, _, _ = multipletests(res_df["p"].values, alpha=0.05, method="fdr_bh")
res_df["p_adj"]    = p_adj
res_df["significant"] = rejected
res_df = res_df.sort_values("p_adj").reset_index(drop=True)
print(f"Significant after FDR (q=0.05): {res_df.significant.sum()} / {len(res_df)}")
res_df"""),

    cell("md", """## 6. Confirmatory regression with interaction

The naive H02 says drive-thru weekend revenue is *lower* (because drive-thru branches sit in lower-prestige districts). But the *weekend lift inside* drive-thru branches may still be larger. This is the kind of finding the sweep alone hides — a confirmatory regression with the right interaction reveals it.
"""),

    cell("code", """# Daily revenue ~ has_drive_thru * is_weekend + controls
model = smf.ols(
    "revenue ~ has_drive_thru * is_weekend + seats + size_sqm + base_traffic + C(district) + promo_active",
    data=panel
).fit()
print(model.summary().tables[1])
print("\\nKey interaction: has_drive_thru:is_weekend  →  the *additional* weekend lift drive-thru branches enjoy on top of non-DT.")"""),

    cell("md", "## 7. Dashboard — significant findings only"),

    cell("code", """sig = res_df[res_df.significant].copy()
sig["abs_effect"] = sig["effect"].abs()
sig = sig.sort_values("abs_effect", ascending=True)

fig, ax = plt.subplots(figsize=(10, max(4, 0.45*len(sig))))
colors = ["#0891B2" if e > 0 else "#DC2626" for e in sig["effect"]]
bars = ax.barh(sig["hypothesis"], sig["effect"], color=colors)
ax.axvline(0, color="#374151", lw=0.5)
ax.set_xlabel("Effect size (Cohen's d / eta² / r)")
ax.set_title("Significant Relationships (FDR q < 0.05)", fontsize=14, fontweight="bold")
for bar, p, summary in zip(bars, sig["p_adj"], sig["summary"]):
    ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
            f"  q={p:.3g}  {summary}", va="center", fontsize=8, color="#374151")
plt.tight_layout()
plt.show()"""),

    cell("md", """## 8. Discussion prompts

1. Which hypotheses survived FDR — and which intuitive ones *failed* to survive?
2. What does the regression interaction tell us that the pairwise sweep didn't?
3. If you had to pick **three** drivers of revenue to optimize, which would you choose, and why?
4. What confounders are still uncontrolled? How would you address them in a follow-up analysis?

**Next:** Module 2 — forecasting SKU × Branch demand for the next 30 days.
"""),
]

write_notebook("01_causal_chain_hypothesis_testing.ipynb", cells)
print("Module 1 notebook written.")
