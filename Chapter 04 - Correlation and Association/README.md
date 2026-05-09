# Chapter 04 — Correlation and Association

Pearson, Spearman, and chi-square on Brew Lab

## Run
- **Local Jupyter** (after cloning the repo): `jupyter notebook` in `notebooks/` and open the `.ipynb`. Make sure you've cloned the full repo so that `Integrated Data Analytics Exercise/data/brewlab.db` exists alongside this folder.
- **Colab**: open the notebook via the badge below. The bootstrap cell clones the repo and installs requirements automatically.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2004%20-%20Correlation%20and%20Association/notebooks/04_correlation_and_association.ipynb)

## What you'll do
Correlation measures the strength of a relationship.

| Variables | Method |
|---|---|
| Two continuous (linear) | Pearson |
| Two continuous (monotonic, robust to outliers) | Spearman |
| Two categorical | Chi-square test of independence |

Each method returns a statistic and a p-value. Always **plot first** — a number without a picture can mislead.

---

Part of MADT6004 — Applied Data Analytics for Business.
