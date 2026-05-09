# Chapter 03 — Group Comparison

t-test, ANOVA, chi-square on Brew Lab branches and channels

## Run
- **Local Jupyter** (after cloning the repo): `jupyter notebook` in `notebooks/` and open the `.ipynb`. Make sure you've cloned the full repo so that `Integrated Data Analytics Exercise/data/brewlab.db` exists alongside this folder.
- **Colab**: open the notebook via the badge below. The bootstrap cell clones the repo and installs requirements automatically.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2003%20-%20Group%20Comparison/notebooks/03_group_comparison.ipynb)

## What you'll do
Three classic tests:

| Comparison | Test |
|---|---|
| Two-group means (one continuous outcome) | t-test |
| Three or more groups (one continuous outcome) | One-way ANOVA |
| Two categorical variables | Chi-square test of independence |

Each gives a **test statistic** and a **p-value**. p < 0.05 → the groups likely differ; otherwise we can't conclude there's a difference.

---

Part of MADT6004 — Applied Data Analytics for Business.
