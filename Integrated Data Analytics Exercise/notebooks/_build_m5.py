"""Build Module 5: Thai text analytics."""
import sys
sys.path.insert(0, ".")
from _nbutil import cell, write_notebook

cells = [
    cell("md", """# Module 5 — Thai Text Analytics
**MADT6004 Wrap-Up · Brew Lab BKK case**

Khun Ploy: *"The numbers say one branch is fine. My gut says it's not. What are customers actually saying — and where is it worst?"*

What you'll do:
1. Load the **Thai + English review corpus**.
2. Tokenize with **PyThaiNLP**, remove stopwords.
3. Build a **bi-gram network graph** of frequent word pairs.
4. Use **POS tagging** to extract entities (nouns) and descriptors (adjectives), then visualize the **entity ↔ adjective network**.
5. Run **topic modeling** (LDA) and surface complaint themes.
6. Cross-tab topics × branch × time → find the **Thonglor leading-indicator**: a branch where complaint volume is rising before ratings drop."""),

    cell("md", """## 1. Setup

PyThaiNLP installation:
```bash
pip install pythainlp
```"""),

    cell("code", """import sqlite3
import warnings
import re
from collections import Counter, defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
warnings.filterwarnings("ignore")
plt.rcParams["figure.dpi"] = 100

import matplotlib
matplotlib.rcParams['font.family'] = ['Noto Sans Thai', 'TH Sarabun New', 'DejaVu Sans']

from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.tag import pos_tag

THAI_STOPS = set(thai_stopwords())
# Add common stop-ish words for our domain
DOMAIN_STOPS = {'ร้าน','สาขา','ที่','นี้','มาก','แต่','ก็','ค่ะ','ครับ',' ','','-','/','(',')','.', ',', ':'}
ALL_STOPS = THAI_STOPS | DOMAIN_STOPS

EN_STOPS = {'the','a','an','at','of','to','in','for','is','was','it','this','that','and','or','but','my','i','very','too','so'}

conn = sqlite3.connect("../data/brewlab.db")
reviews = pd.read_sql("SELECT * FROM reviews", conn)
reviews['review_date'] = pd.to_datetime(reviews['review_date'])
print(f"Total reviews: {len(reviews)}")
print(reviews.head(3)[['review_id','branch_id','rating','sentiment_label','text']])"""),

    cell("md", "## 2. Tokenize and clean"),

    cell("code", """def tokenize_thai_en(text):
    \"\"\"Mixed Thai + English tokenizer with cleaning.\"\"\"
    if not isinstance(text, str):
        return []
    # PyThaiNLP handles Thai segmentation; for English mixed in, it produces tokens too
    tokens = word_tokenize(text, engine='newmm')
    out = []
    for tok in tokens:
        tok = tok.strip().lower()
        if not tok or tok in ALL_STOPS or tok in EN_STOPS:
            continue
        if re.fullmatch(r'[\\d\\W_]+', tok):  # all digits/punct
            continue
        if len(tok) == 1 and not re.match(r'[ก-๙]', tok):
            continue
        out.append(tok)
    return out

reviews['tokens'] = reviews['text'].apply(tokenize_thai_en)
print("Sample tokenization:")
for i in range(3):
    print(f"  text   : {reviews['text'].iloc[i]}")
    print(f"  tokens : {reviews['tokens'].iloc[i]}")
    print()"""),

    cell("md", "## 3. Word frequency"),

    cell("code", """all_tokens = [t for toks in reviews['tokens'] for t in toks]
freq = Counter(all_tokens)
top = pd.DataFrame(freq.most_common(30), columns=['token','count'])
fig, ax = plt.subplots(figsize=(8,6))
sns.barplot(data=top, y='token', x='count', color='#0891B2', ax=ax)
ax.set_title("Top 30 tokens (cleaned)")
plt.tight_layout(); plt.show()"""),

    cell("md", "## 4. Bi-gram network graph"),

    cell("code", """def bigrams(tokens):
    return list(zip(tokens[:-1], tokens[1:]))

bg = Counter()
for toks in reviews['tokens']:
    bg.update(bigrams(toks))

# Filter for meaningful pairs
top_bg = [(a, b, c) for (a, b), c in bg.most_common() if c >= 8 and a != b]
print(f"Top bi-grams (count >= 8): {len(top_bg)}")
bg_df = pd.DataFrame(top_bg[:30], columns=['word1','word2','count'])
print(bg_df.head(15))"""),

    cell("code", """# Build network
G = nx.Graph()
for w1, w2, c in top_bg[:60]:
    if G.has_edge(w1, w2):
        G[w1][w2]['weight'] += c
    else:
        G.add_edge(w1, w2, weight=c)

fig, ax = plt.subplots(figsize=(13,9))
pos = nx.spring_layout(G, k=0.6, iterations=80, seed=42)
node_size = [freq[n]*3 + 100 for n in G.nodes()]
edges = list(G.edges(data=True))
weights = [d['weight'] for _,_,d in edges]
maxw = max(weights) if weights else 1
nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color='#0891B2', alpha=0.85, ax=ax)
nx.draw_networkx_edges(G, pos, width=[w/maxw*4 for w in weights], alpha=0.4, edge_color='#374151', ax=ax)
nx.draw_networkx_labels(G, pos, font_size=10)
ax.set_title("Bi-gram Network — review co-occurrence", fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout(); plt.show()"""),

    cell("md", """## 5. POS tagging — extract entities (nouns) and adjectives

PyThaiNLP's POS tagger uses the **ORCHID tagset**:
- `NCMN`, `NPRP`, `NTTL` — nouns (common, proper, title) → **entities**
- `VATT`, `ADVN`, `ADJX` — adjective-like → **descriptors**

We extract noun-adjective co-occurrences within each review and visualize the network.

(Optional: PyThaiNLP also has a NER engine — `from pythainlp.tag.named_entity import NER` — but it requires a corpus download. POS-based extraction is the dependable path.)"""),

    cell("code", """NOUN_TAGS = {'NCMN','NPRP','NTTL','NLBL','NONM'}
ADJ_TAGS  = {'VATT','ADJX','ADVN','ADVI','ADVP'}

def extract_noun_adj(tokens):
    if not tokens:
        return [], []
    tagged = pos_tag(tokens)
    nouns = [w for w, t in tagged if t in NOUN_TAGS]
    adjs  = [w for w, t in tagged if t in ADJ_TAGS]
    return nouns, adjs

reviews[['nouns','adjs']] = reviews['tokens'].apply(
    lambda x: pd.Series(extract_noun_adj(x), index=['nouns','adjs']))

# Build noun–adjective co-occurrence (within the same review)
na_pairs = Counter()
for _, row in reviews.iterrows():
    for n in row['nouns']:
        for a in row['adjs']:
            na_pairs[(n, a)] += 1

print(f"Unique noun-adjective pairs: {len(na_pairs)}")
print("Top 20 entity ↔ adjective pairs:")
for (n, a), c in na_pairs.most_common(20):
    print(f"  {n:20} ↔ {a:15} {c}")"""),

    cell("code", """# Network: nouns (entities) ↔ adjectives (descriptors)
G2 = nx.Graph()
for (n, a), c in na_pairs.most_common(60):
    G2.add_node(n, kind='entity')
    G2.add_node(a, kind='adj')
    G2.add_edge(n, a, weight=c)

fig, ax = plt.subplots(figsize=(13, 9))
pos = nx.spring_layout(G2, k=0.7, iterations=80, seed=42)
ent = [n for n, d in G2.nodes(data=True) if d['kind']=='entity']
adj = [n for n, d in G2.nodes(data=True) if d['kind']=='adj']
nx.draw_networkx_nodes(G2, pos, nodelist=ent, node_color='#0891B2',
                       node_size=400, alpha=0.85, ax=ax)
nx.draw_networkx_nodes(G2, pos, nodelist=adj, node_color='#D97706',
                       node_size=300, alpha=0.85, ax=ax)
weights = [d['weight'] for _,_,d in G2.edges(data=True)]
maxw = max(weights) if weights else 1
nx.draw_networkx_edges(G2, pos, width=[w/maxw*3 for w in weights],
                       alpha=0.35, ax=ax)
nx.draw_networkx_labels(G2, pos, font_size=9)
ax.set_title("Entity ↔ Adjective Network (teal=entity, amber=adjective)",
             fontsize=13, fontweight='bold')
ax.axis('off')
plt.tight_layout(); plt.show()"""),

    cell("md", """## 6. Topic modeling — LDA

Latent Dirichlet Allocation finds groups of words that co-occur. We tune `n_topics` to surface the latent themes."""),

    cell("code", """from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Build a "joined" token document for sklearn
docs = reviews['tokens'].apply(lambda toks: ' '.join(toks)).tolist()

cv = CountVectorizer(min_df=5, max_df=0.6, token_pattern=r'\\S+')
X = cv.fit_transform(docs)
vocab = cv.get_feature_names_out()
print(f"Vocab size: {len(vocab)}, doc-term matrix: {X.shape}")

K = 5
lda = LatentDirichletAllocation(n_components=K, random_state=42, max_iter=20, learning_method='online')
doc_topic = lda.fit_transform(X)

print(f"\\nTopics ({K}):")
for k, comp in enumerate(lda.components_):
    top_words = [vocab[i] for i in comp.argsort()[-12:][::-1]]
    print(f"  Topic {k}: {' / '.join(top_words)}")"""),

    cell("md", "## 7. Topic × branch × time — the Thonglor leading indicator"),

    cell("code", """# Assign each review its dominant topic
reviews['topic'] = doc_topic.argmax(axis=1)
reviews['month'] = reviews['review_date'].dt.to_period('M').astype(str)

branches = pd.read_sql("SELECT branch_id, name AS branch FROM branches", conn)
reviews_b = reviews.merge(branches, on='branch_id')

# Heatmap: branch × topic
ct = pd.crosstab(reviews_b['branch'], reviews_b['topic'], normalize='index')
fig, ax = plt.subplots(figsize=(10, 5))
sns.heatmap(ct, annot=True, fmt=".2f", cmap="Blues", ax=ax,
            cbar_kws={'label':'share of reviews'})
ax.set_title("Topic share by branch (rows sum to 1)")
ax.set_xlabel("Topic")
plt.tight_layout(); plt.show()"""),

    cell("code", """# Negative sentiment volume by branch over time
neg = reviews_b[reviews_b['sentiment_label'] == 'negative']
neg_pivot = neg.groupby(['month','branch']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(12, 5))
for col in neg_pivot.columns:
    is_thonglor = col == 'Thonglor'
    ax.plot(neg_pivot.index, neg_pivot[col],
            marker='o' if is_thonglor else None,
            lw=2.5 if is_thonglor else 1,
            color='#DC2626' if is_thonglor else '#9CA3AF',
            label=col, alpha=1 if is_thonglor else 0.5)
ax.set_title("Negative review volume by branch over time — Thonglor highlighted",
             fontsize=12, fontweight='bold')
ax.set_xlabel("Month"); ax.set_ylabel("# negative reviews")
ax.tick_params(axis='x', rotation=45)
ax.legend(loc='upper left', fontsize=8, ncol=3)
plt.tight_layout(); plt.show()"""),

    cell("code", """# Compare avg rating vs negative review share for Thonglor in last 6 weeks vs prior
thg = reviews_b[reviews_b['branch']=='Thonglor'].copy()
recent = thg[thg['review_date'] >= '2026-03-19']
prior  = thg[thg['review_date'] <  '2026-03-19']
print(f"Thonglor — recent (last 6w): rating={recent['rating'].mean():.2f}, "
      f"neg share={(recent['sentiment_label']=='negative').mean()*100:.0f}%, n={len(recent)}")
print(f"Thonglor — prior        : rating={prior['rating'].mean():.2f}, "
      f"neg share={(prior['sentiment_label']=='negative').mean()*100:.0f}%, n={len(prior)}")
print()
print("→ Negative volume rising sharply, but average rating only modestly affected.")
print("  This is a leading indicator: complaint volume moves before star rating.")"""),

    cell("md", """## 8. Sentiment score back into Module 3

The sentiment score (or topic share) per customer can be added as a feature to Module 3's churn / response classifier. Watch the AUC move."""),

    cell("code", """# Compute customer-level sentiment summary
cust_sent = reviews.groupby('customer_id').agg(
    n_reviews=('review_id','size'),
    pct_negative=('sentiment_label', lambda s: (s=='negative').mean()),
    avg_rating=('rating','mean')
).reset_index()
print("Customer-level sentiment features (sample):")
print(cust_sent.head())
print(f"\\n{len(cust_sent)} customers have written reviews. "
      f"This becomes a join key for Module 3's feature table.")"""),

    cell("md", """## 9. Discussion prompts

1. The bi-gram network surfaces **what people say together**. The entity-adjective network surfaces **what they call things**. Which is more actionable for ops?
2. The Thonglor pattern is the kind of **leading indicator** that quantitative dashboards miss. How would you institutionalize this — sentiment monitoring as an early-warning system?
3. POS-based "NER" is good enough for branches and product names. When would you invest in a real NER model?
4. Topic modeling assigns one dominant topic per review. What's lost? How would you handle reviews that span multiple complaints?

## End of integrated exercise

Looking back across all five modules, you've gone from raw transactions to a defensible decision system:

- **Module 1** told us *what's actually true* about revenue drivers (with FDR control).
- **Module 2** told us *what's coming* (per SKU per branch).
- **Module 3** told us *who to target* (with proper sampling for class imbalance).
- **Module 4** told us *how customers cluster and what to recommend*.
- **Module 5** told us *what they're saying* — and surfaced a leading indicator the numbers missed.

The loop closes when Module 5's sentiment score becomes a feature in Module 3, and Module 4's segments become targeting filters. **This is what real practice looks like.**"""),
]

write_notebook("05_thai_text_analytics.ipynb", cells)
print("Module 5 notebook written.")
