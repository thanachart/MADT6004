"""Build Module 3 notebook: campaign response classification."""
import sys
sys.path.insert(0, ".")
from _nbutil import cell, write_notebook

cells = [
    cell("md", """# Module 3 — Campaign Response Classification
**MADT6004 Wrap-Up · Brew Lab BKK case**

Khun Ploy: *"We sent the Comeback 50 voucher to lapsed members. Some responded, most didn't. Of the **next** lapsed batch, who should I target?"*

What you'll do:
1. Build the modeling table — features for each customer who got the campaign + their response label.
2. Run a **grid of (sampling × algorithm)** combinations:
   - Sampling: **none / under / over / SMOTE**
   - Algorithms: **Decision Tree / Logistic Regression / SVM / Random Forest / XGBoost**
3. Use a proper **train / validation / test** split.
4. Report **F1, Precision, Recall, ROC-AUC** for every combination.
5. Build a **lift-by-decile table** for the winning model.

The base response rate is ~11% — imbalanced enough that sampling will matter."""),

    cell("md", "## 1. Setup"),

    cell("code", """import sqlite3
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings("ignore")
plt.rcParams["figure.dpi"] = 100
sns.set_style("whitegrid")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score, classification_report
from xgboost import XGBClassifier

from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler, SMOTE

conn = sqlite3.connect("../data/brewlab.db")"""),

    cell("md", "## 2. Build the modeling table"),

    cell("code", """# Snapshot date — we know who was lapsed by 2026-04-24, sent on 2026-04-25
SNAPSHOT = "2026-04-24"

# Customer features as of the snapshot
features = pd.read_sql(f'''
WITH txn_window AS (
  SELECT customer_id,
         COUNT(*)                                       AS frequency,
         SUM(total)                                     AS monetary,
         AVG(total)                                     AS avg_ticket,
         julianday('{SNAPSHOT}') - julianday(MAX(date(datetime))) AS recency,
         julianday(MAX(date(datetime))) - julianday(MIN(date(datetime))) AS tenure_active,
         SUM(CASE WHEN channel='app'      THEN 1 ELSE 0 END)*1.0/COUNT(*) AS app_share,
         SUM(CASE WHEN channel='delivery' THEN 1 ELSE 0 END)*1.0/COUNT(*) AS delivery_share,
         SUM(CASE WHEN promo_id IS NOT NULL THEN 1 ELSE 0 END)*1.0/COUNT(*) AS promo_share
  FROM transactions
  WHERE date(datetime) <= '{SNAPSHOT}'
  GROUP BY customer_id
)
SELECT cr.customer_id, cr.responded,
       c.age_group, c.gender, c.home_district, c.acquisition_channel, c.segment,
       julianday('{SNAPSHOT}') - julianday(c.signup_date) AS tenure_days,
       tw.frequency, tw.monetary, tw.avg_ticket, tw.recency,
       tw.app_share, tw.delivery_share, tw.promo_share
FROM campaign_responses cr
JOIN customers c USING(customer_id)
LEFT JOIN txn_window tw USING(customer_id)
''', conn)
print("Modeling table:", features.shape)
print("Class balance:", features.responded.value_counts(normalize=True).to_dict())
features.head()"""),

    cell("md", "## 3. Train / Validation / Test split (60 / 20 / 20)"),

    cell("code", """y = features['responded'].values
X = features.drop(columns=['customer_id', 'responded'])

# Train+temp = 80%, then split temp 50/50 to get 60/20/20
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42, stratify=y)
X_val,   X_test, y_val,   y_test  = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

print(f"Train: {len(X_train)}  ({y_train.mean()*100:.1f}% positive)")
print(f"Val  : {len(X_val)}  ({y_val.mean()*100:.1f}% positive)")
print(f"Test : {len(X_test)}  ({y_test.mean()*100:.1f}% positive)")"""),

    cell("md", """## 4. Preprocessing pipeline

Numeric → standardize. Categorical → one-hot. Then we can swap any classifier downstream."""),

    cell("code", """num_cols = ['tenure_days','frequency','monetary','avg_ticket','recency',
            'app_share','delivery_share','promo_share']
cat_cols = ['age_group','gender','home_district','acquisition_channel','segment']

prep = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
])

# Fit prep on train only, transform val + test
prep.fit(X_train)
Xtr = prep.transform(X_train); Xv = prep.transform(X_val); Xte = prep.transform(X_test)
print("Train matrix shape:", Xtr.shape)"""),

    cell("md", """## 5. The grid: sampling × algorithm

We loop over all combinations and record metrics on the validation set."""),

    cell("code", """SAMPLERS = {
    "none":  None,
    "under": RandomUnderSampler(random_state=42),
    "over":  RandomOverSampler(random_state=42),
    "smote": SMOTE(random_state=42, k_neighbors=5),
}

ALGORITHMS = {
    "decision_tree":     lambda: DecisionTreeClassifier(max_depth=6, random_state=42),
    "logistic":          lambda: LogisticRegression(max_iter=2000, random_state=42),
    "svm_rbf":           lambda: SVC(probability=True, random_state=42),
    "random_forest":     lambda: RandomForestClassifier(n_estimators=200, max_depth=8, random_state=42, n_jobs=-1),
    "xgboost":           lambda: XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.05,
                                                use_label_encoder=False, eval_metric='logloss',
                                                random_state=42, n_jobs=-1),
}"""),

    cell("md", "## 6. The loop function — train every (sampler, algorithm) pair"),

    cell("code", """def evaluate(model, X, y):
    pred = model.predict(X)
    proba = model.predict_proba(X)[:,1] if hasattr(model, "predict_proba") else None
    return {
        "f1":        f1_score(y, pred, zero_division=0),
        "precision": precision_score(y, pred, zero_division=0),
        "recall":    recall_score(y, pred, zero_division=0),
        "auc":       roc_auc_score(y, proba) if proba is not None else np.nan,
    }

def run_grid(Xtr, ytr, Xv, yv, samplers, algorithms):
    rows = []
    for s_name, sampler in samplers.items():
        if sampler is None:
            Xtr_s, ytr_s = Xtr, ytr
        else:
            Xtr_s, ytr_s = sampler.fit_resample(Xtr, ytr)
        for a_name, make_alg in algorithms.items():
            model = make_alg()
            model.fit(Xtr_s, ytr_s)
            m = evaluate(model, Xv, yv)
            m.update({"sampling": s_name, "algorithm": a_name,
                      "n_train_after_sampling": len(ytr_s),
                      "pos_rate_after": float(np.mean(ytr_s))})
            rows.append(m)
    return pd.DataFrame(rows)

grid = run_grid(Xtr, y_train, Xv, y_val, SAMPLERS, ALGORITHMS)
grid_view = grid[['sampling','algorithm','pos_rate_after','f1','precision','recall','auc']].sort_values('auc', ascending=False)
print("Validation metrics — sorted by AUC:")
grid_view"""),

    cell("md", "## 7. Heatmap of AUC across the grid"),

    cell("code", """pv = grid.pivot(index='algorithm', columns='sampling', values='auc')
fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(pv, annot=True, fmt=".3f", cmap="Greens", ax=ax, cbar_kws={'label':'AUC'})
ax.set_title("Validation AUC by (Sampling × Algorithm)")
plt.tight_layout(); plt.show()"""),

    cell("md", "## 8. Lock the winner, evaluate on the held-out test set"),

    cell("code", """winner = grid.sort_values('auc', ascending=False).iloc[0]
print("Winner on validation:", winner[['sampling','algorithm','auc','f1']].to_dict())

s = SAMPLERS[winner['sampling']]
if s is None:
    Xtrf, ytrf = Xtr, y_train
else:
    Xtrf, ytrf = s.fit_resample(Xtr, y_train)

best_model = ALGORITHMS[winner['algorithm']]()
best_model.fit(Xtrf, ytrf)

test_metrics = evaluate(best_model, Xte, y_test)
print("\\nTEST set performance:")
for k, v in test_metrics.items():
    print(f"  {k}: {v:.3f}")
test_proba = best_model.predict_proba(Xte)[:,1]"""),

    cell("md", """## 9. Lift by decile

We sort the test set by predicted probability, split into deciles, and compute response rate per decile vs the overall base rate. The **cumulative lift** tells the campaign manager: *"if we target the top 30% of scored customers, we capture X% of total responders at Y× the base rate."*"""),

    cell("code", """def lift_decile_table(y_true, y_proba, n_buckets=10):
    df = pd.DataFrame({'y': y_true, 'p': y_proba}).sort_values('p', ascending=False).reset_index(drop=True)
    df['decile'] = pd.qcut(df.index, n_buckets, labels=False) + 1
    base_rate = df['y'].mean()
    g = df.groupby('decile').agg(
        n=('y','size'),
        responders=('y','sum'),
    )
    g['response_rate'] = g['responders'] / g['n']
    g['lift']         = g['response_rate'] / base_rate
    g['cum_responders'] = g['responders'].cumsum()
    g['cum_n']          = g['n'].cumsum()
    g['cum_response_rate'] = g['cum_responders'] / g['cum_n']
    g['cum_lift']        = g['cum_response_rate'] / base_rate
    g['capture_rate']    = g['cum_responders'] / df['y'].sum()
    return g.reset_index()

lift = lift_decile_table(y_test, test_proba)
print(f"Base rate: {y_test.mean()*100:.1f}%")
lift.round(3)"""),

    cell("code", """# Cumulative gains + lift chart
fig, axes = plt.subplots(1, 2, figsize=(13, 4))
axes[0].plot([0]+list(lift['decile']), [0]+list(lift['capture_rate']*100), marker='o', color='#0891B2', label='Model')
axes[0].plot([0,10],[0,100], '--', color='#9CA3AF', label='Random')
axes[0].set_xlabel("Decile (top N deciles targeted)")
axes[0].set_ylabel("% of total responders captured")
axes[0].set_title("Cumulative Gains")
axes[0].legend()

axes[1].bar(lift['decile'], lift['lift'], color='#0891B2')
axes[1].axhline(1, color='#374151', lw=0.7)
axes[1].set_xlabel("Decile (1 = top scored)")
axes[1].set_ylabel("Lift over base rate")
axes[1].set_title("Lift by Decile")
plt.tight_layout(); plt.show()"""),

    cell("md", """## 10. Operational read

If we send the comeback voucher to **the top 30% of scored customers**, we capture the lift shown above at a fraction of the cost of mass-sending. Decision threshold should be set by **expected profit** — voucher cost × responders − margin loss × non-responders.

## Discussion prompts

1. Did sampling actually move AUC, or did a strong model recover signal without it? When is sampling worth the complexity?
2. Why is **Recall** the more honest metric for this problem than Accuracy?
3. How would you set the **decision threshold** (top-N% to target) to maximize profit?
4. Imagine the response rate were 1% instead of 11% — which sampler would matter most?

**Next:** Module 4 — customer single view, segmentation, and a recommendation engine."""),
]

write_notebook("03_campaign_response_classification.ipynb", cells)
print("Module 3 notebook written.")
