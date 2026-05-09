# Chapter 05b — Time Series

Trend, seasonality, and naive forecasts on daily revenue

## Run
- **Local Jupyter** (after cloning the repo): `jupyter notebook` in `notebooks/` and open the `.ipynb`. Make sure you've cloned the full repo so that `Integrated Data Analytics Exercise/data/brewlab.db` exists alongside this folder.
- **Colab**: open the notebook via the badge below. The bootstrap cell clones the repo and installs requirements automatically.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2005b%20-%20Time%20Series/notebooks/05b_time_series.ipynb)

## What you'll do
A time series has two big components:
- **Trend** — the long-run direction
- **Seasonality** — repeating patterns (weekly, monthly)

Three baseline forecasts every analyst should know:
1. **Naive** — tomorrow = today
2. **Seasonal naive** — next Monday = last Monday
3. **Holt-Winters** — additive trend + seasonal smoothing

Always compare your fancy model against the baselines.

---

Part of MADT6004 — Applied Data Analytics for Business.
