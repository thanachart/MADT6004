# Integrated Data Analytics Exercise

**MADT6004 — Applied Data Analytics for Business · Wrap-Up Session**

A 3-hour integrated demo that takes one fictional Bangkok coffee chain — **Brew Lab BKK** — through the full analytics journey: from raw transactions to a defensible decision system.

The five modules close a loop. Module 5's sentiment becomes a feature in Module 3. Module 4's segments become targeting filters. By the end, students see how techniques they learned in isolation across the semester actually plug into one another in practice.

---

## The case

Brew Lab BKK is a 12-branch specialty coffee chain across Bangkok with ~5,000 active loyalty members and 12 months of transaction history (May 2025 – April 2026). The COO, **Khun Ploy**, has five questions she needs answered:

| # | Question | Module | Technique |
|---|----------|--------|-----------|
| 1 | What actually drives daily branch revenue? | 01 | Causal-chain hypothesis sweep + FDR + interaction regression |
| 2 | How much will each SKU sell at each branch over the next 30 days? | 02 | Batch forecasting (Naive / Seasonal Naive / Holt-Winters) |
| 3 | Of the next batch of lapsed members, who will respond to the comeback voucher? | 03 | Imbalanced classification with sampling × algorithm grid |
| 4 | How many real *types* of customer do we have, and what should we put in front of them? | 04 | Customer single view → k-means → item-item recommendation |
| 5 | What are customers actually saying — and where is it worst? | 05 | Thai text analytics: tokenization, bi-gram + entity-adjective networks, LDA |

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/thanachart/MADT6004.git
cd "MADT6004/Integrated Data Analytics Exercise"
pip install -r requirements.txt
```

### 2. Generate the dataset

The SQLite file is committed in `data/brewlab.db` (~58 MB). If you want to regenerate from scratch (different seed, different patterns):

```bash
cd data
python generate_data.py
```

This produces `brewlab.db` with engineered patterns guaranteed to surface signal in every module. The generator is fully reproducible (seed = `20260508`).

### 3. Run the notebooks in order

```bash
cd notebooks
jupyter notebook
```

Open and run notebooks **01 → 05** in sequence. Each is self-contained but they tell a continuous story. Each notebook ends with discussion prompts intended for class conversation.

---

## What's in `data/brewlab.db`

| Table | Rows | Description |
|-------|------|-------------|
| `branches` | 12 | Branch attributes: district, drive-thru, seats, size, base traffic |
| `customers` | 5,000 | Demographics + acquisition channel + engineered segment label |
| `products` | 40 | Coffee, tea, food, dessert, merch with price + cost |
| `transactions` | ~267,000 | Order-level, 12 months, branch + customer + channel + promo + total |
| `order_items` | ~362,000 | Line-level: product, qty, unit price, line discount |
| `promotions` | 8 | Includes the *Comeback 50* voucher campaign |
| `loyalty_events` | ~273,000 | Per-customer event log: signup / visit / lapse |
| `campaign_responses` | 874 | *Comeback 50* sent to lapsed members. ~11% responded — imbalanced. |
| `reviews` | 1,835 | Thai + English mixed with rating + sentiment label |

---

## Engineered signal — what each module finds

The data is *not* random. Patterns are seeded so that running the analysis surfaces real, defensible findings. Highlights:

- **Module 1** — drive-thru branches earn lower revenue *overall* (lower-prestige districts) but have a *larger weekend lift*. The naive t-test gets it wrong; the regression interaction reveals the truth. Teaching gold.
- **Module 2** — strong weekly seasonality + mild upward trend. Seasonal naive often beats Holt-Winters on small SKUs.
- **Module 3** — 11% positive class. SMOTE + XGBoost typically wins. Top-decile lift is ~2.5–3×.
- **Module 4** — k-means cleanly recovers the four engineered segments (Daily Loyalist, Weekend Bruncher, App Promo Hunter, Casual Drifter).
- **Module 5** — Thonglor branch shows a **leading indicator**: negative review volume spikes from ~23% to ~63% in the last six weeks while average rating stays flat. Numbers say everything's fine. Reviews say it isn't.

---

## How the modules connect

```
[Module 1]              [Module 2]              [Module 5]
Hypothesis sweep   →    Forecast demand    ←    Sentiment + topics
       ↓                       ↓                       ↓
   what's true            what's coming        what they're saying
                              ↓                       ↓
                        [Module 3] ←──────── (sentiment as feature)
                        Who responds
                              ↓
                        [Module 4] ←──────── (segment as filter)
                        Who they are + what to recommend
```

The integration thread is what students take away: the techniques are not silos — they compose.

---

## File layout

```
Integrated Data Analytics Exercise/
├── README.md                       # this file
├── requirements.txt                # Python dependencies
├── data/
│   ├── generate_data.py            # reproducible data generator
│   └── brewlab.db                  # SQLite (58 MB)
├── notebooks/
│   ├── 01_causal_chain_hypothesis_testing.ipynb
│   ├── 02_batch_forecasting_sku_branch.ipynb
│   ├── 03_campaign_response_classification.ipynb
│   ├── 04_segmentation_recommendation.ipynb
│   ├── 05_thai_text_analytics.ipynb
│   └── _nbutil.py                  # internal: notebook builder helper
└── slides/
    └── MADT6004_Wrap_Up_Session.pptx
```

---

## Suggested time budget — 3-hour session

| Time | Section |
|------|---------|
| 5 min | Cold open — Khun Ploy's panic, the five questions |
| 50 min | **Module 1** — hypothesis sweep, FDR, interaction reveal |
| 55 min | **Module 2** — forecast loop, RMSE comparison, the 30-day output |
| 30 min | **Module 3** — sampling × algorithm grid, lift table |
| 30 min | **Module 4** — single view, segments, recommendation network |
| 25 min | **Module 5** — Thai tokenization, bi-gram net, the Thonglor reveal |
| 15 min | Close — loop closes, integration thread, "this is real practice" |

---

## Notes for instructors

- **PyThaiNLP NER** requires a corpus download (`pythainlp data get thainer-1.4`). The notebook falls back to POS-based noun/adjective extraction, which works without internet and is good enough for the demonstration.
- **XGBoost** in Module 3 trains in seconds even with the SMOTE × algorithm grid. If a student's machine is slow, drop SVM (it's the slowest).
- **Thai font rendering** in matplotlib may need a font install on macOS/Windows. The notebook sets `Noto Sans Thai` with `DejaVu Sans` fallback; on Thai-keyboard machines it usually just works.
- The notebooks are designed for **vibe-coding live demo** mode — instructors can run them as-is, or use them as a *target output* while live-prompting an AI assistant to recreate the analyses.

---

## Author

**Asst. Prof. Dr. Thanachart Ritbumroong**
Program Director, MADT — NIDA
Built as part of MADT6004 wrap-up materials, May 2026.
