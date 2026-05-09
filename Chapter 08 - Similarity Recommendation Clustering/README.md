# Chapter 08 — Similarity, Recommendation, Clustering

k-means on customers + item-item recommendation

## Run
- **Local Jupyter** (after cloning the repo): `jupyter notebook` in `notebooks/` and open the `.ipynb`. Make sure you've cloned the full repo so that `Integrated Data Analytics Exercise/data/brewlab.db` exists alongside this folder.
- **Colab**: open the notebook via the badge below. The bootstrap cell clones the repo and installs requirements automatically.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/thanachart/MADT6004/blob/main/Chapter%2008%20-%20Similarity%20Recommendation%20Clustering/notebooks/08_similarity_recommendation_clustering.ipynb)

## What you'll do
Two related ideas in unsupervised learning:

- **Clustering** — group similar customers so you can talk about "types"
- **Recommendation** — measure similarity between *items* and recommend products that go together

You will:
1. Build a customer single-view (RFM-like features)
2. Run k-means and pick k by silhouette
3. Compute item-item cosine similarity from co-purchase patterns

---

Part of MADT6004 — Applied Data Analytics for Business.
