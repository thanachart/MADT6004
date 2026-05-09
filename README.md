# MADT6004 — Applied Data Analytics for Business

Course materials for **MADT6004 · Applied Data Analytics for Business** at NIDA's MADT program. Every notebook in this repo runs against the same fictional case — **Brew Lab BKK**, a 12-branch specialty coffee chain in Bangkok with 12 months of transaction history.

The dataset (`brewlab.db`) is engineered with realistic patterns: weekly seasonality, branch-format effects, an imbalanced campaign-response problem, mixed Thai/English reviews. One database, every chapter.

---

## How the materials are organized

| Folder | Use it for |
|---|---|
| `Integrated Data Analytics Exercise/` | The 3-hour wrap-up session — five connected modules that take Brew Lab from raw transactions to a decision system. The `brewlab.db` and `requirements.txt` live here. |
| `Chapter 01 — 08/` | One focused exercise notebook per syllabus chapter. Each chapter notebook reuses `Integrated Data Analytics Exercise/data/brewlab.db` so students learn the techniques on the same data, then see them composed in the wrap-up. |

---

## Chapter exercises

Each chapter has a self-contained notebook with a brief intro, hands-on exercises, and discussion prompts.

| # | Topic | Open |
|---|---|---|
| 01 | Introduction to Data Analytics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2001%20-%20Introduction/notebooks/01_introduction.ipynb) |
| 02 | Exploratory Data Analysis | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2002%20-%20EDA/notebooks/02_eda.ipynb) |
| 03 | Group Comparison | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2003%20-%20Group%20Comparison/notebooks/03_group_comparison.ipynb) |
| 04 | Correlation and Association | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2004%20-%20Correlation%20and%20Association/notebooks/04_correlation_and_association.ipynb) |
| 05a | Regression | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2005a%20-%20Regression/notebooks/05a_regression.ipynb) |
| 05b | Time Series | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2005b%20-%20Time%20Series/notebooks/05b_time_series.ipynb) |
| 06 | Classification | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2006%20-%20Classification/notebooks/06_classification.ipynb) |
| 07a | Classification Model Evaluation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2007a%20-%20Classification%20Evaluation/notebooks/07a_classification_evaluation.ipynb) |
| 07b | Text Analytics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2007b%20-%20Text%20Analytics/notebooks/07b_text_analytics.ipynb) |
| 08 | Similarity, Recommendation, Clustering | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2008%20-%20Similarity%20Recommendation%20Clustering/notebooks/08_similarity_recommendation_clustering.ipynb) |

## Integrated Wrap-Up Exercise

Five linked modules that close the loop across the chapters above:

1. Causal-chain hypothesis sweep + interaction regression
2. Batch SKU × branch forecasting (Naive / Seasonal Naive / Holt-Winters)
3. Imbalanced campaign-response classification (sampling × algorithm grid)
4. Customer single view → k-means → item-item recommendation
5. Thai text analytics (tokenization, networks, topic-style summary)

See [`Integrated Data Analytics Exercise/README.md`](Integrated%20Data%20Analytics%20Exercise/README.md) for the full setup and per-module Colab badges.

---

## Running the notebooks

### Colab (recommended)
Click any badge above. The first cell of every notebook bootstraps itself:
- clones this repo into the Colab runtime so `brewlab.db` is available
- `pip install -r requirements.txt`
- changes into the notebooks folder so relative paths resolve

If Colab can't open a notebook from GitHub (a known Colab bug with URL-encoded spaces in folder names): [download the whole repo as a ZIP](https://github.com/thanachart/MADT6004/archive/refs/heads/main.zip), unzip, then upload to your Drive and open from there.

### Local Jupyter
```bash
git clone https://github.com/thanachart/MADT6004.git
cd MADT6004
pip install -r "Integrated Data Analytics Exercise/requirements.txt"
jupyter notebook
```
Open any chapter's `.ipynb` and run all cells.

---

## What's in `brewlab.db`

| Table | Rows | Description |
|---|---|---|
| `branches` | 12 | district, drive-thru, seats, size, base traffic |
| `customers` | 5,000 | demographics + acquisition channel + segment |
| `products` | 40 | coffee, tea, food, dessert, merch — with price + cost |
| `transactions` | ~267,000 | order-level: branch + customer + channel + promo + total |
| `order_items` | ~362,000 | line-level: product, qty, unit price, line discount |
| `promotions` | 8 | includes the *Comeback 50* voucher campaign |
| `loyalty_events` | ~273,000 | per-customer event log: signup / visit / lapse |
| `campaign_responses` | 874 | *Comeback 50* sent to lapsed members; ~11% responded |
| `reviews` | 1,835 | Thai + English mixed with rating + sentiment label |

All tables join on `branch_id` / `customer_id` / `product_id` / `promo_id`.

---

## Author

**Asst. Prof. Dr. Thanachart Ritbumroong**
Program Director, MADT — NIDA
