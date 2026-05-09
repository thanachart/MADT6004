# Chapter 07a — Classification Model Evaluation

Confusion matrix, precision/recall, ROC, lift

## Run
- **Local Jupyter** (after cloning the repo): `jupyter notebook` in `notebooks/` and open the `.ipynb`. Make sure you've cloned the full repo so that `Integrated Data Analytics Exercise/data/brewlab.db` exists alongside this folder.
- **Colab**: open the notebook via the badge below. The bootstrap cell clones the repo and installs requirements automatically.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2007a%20-%20Classification%20Evaluation/notebooks/07a_classification_evaluation.ipynb)

## What you'll do
For an imbalanced problem like *Comeback 50* (only ~11% respond), accuracy is a bad scorecard. The right tools:

- **Confusion matrix** — TP, FP, FN, TN
- **Precision / Recall / F1** — what each error costs you
- **ROC curve & AUC** — ranking quality across all thresholds
- **Lift chart** — for targeting decisions: how many responders do you catch in the top-decile?

---

Part of MADT6004 — Applied Data Analytics for Business.
