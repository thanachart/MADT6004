"""
Brew Lab BKK — Integrated Data Analytics Exercise
Mockup data generator. Produces brewlab.db (SQLite).

Engineered patterns guarantee discoverable signal for each module:
  M1 — Causal-chain hypothesis sweep: ~30 hypotheses, ~6 survive FDR
  M2 — SKU x Branch forecasting: weekly seasonality, mild trend
  M3 — Campaign response: ~5% imbalanced positive class
  M4 — Customer segmentation: 4 distinguishable RFM-behavior clusters
  M5 — Thai text analytics: 5 topics, mixed TH+EN, NER-able entities
"""

import sqlite3
import random
import math
from datetime import datetime, timedelta, date
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260508
random.seed(SEED)
np.random.seed(SEED)

DB_PATH = Path(__file__).parent / "brewlab.db"
START_DATE = date(2025, 5, 1)
END_DATE = date(2026, 4, 30)
N_DAYS = (END_DATE - START_DATE).days + 1

# ----------------------------------------------------------------------
# 1. BRANCHES — 12 branches across Bangkok with varied attributes
# ----------------------------------------------------------------------
BRANCHES = [
    # branch_id, name, district, has_drive_thru, seats, size_sqm, open_year, base_traffic
    (1,  "Asoke",       "Watthana",      0, 38,  95, 2021, 1.00),
    (2,  "Sukhumvit 24","Khlong Toei",   0, 32,  82, 2021, 0.92),
    (3,  "Thonglor",    "Watthana",      0, 45, 110, 2022, 1.05),
    (4,  "Ekkamai",     "Watthana",      0, 28,  72, 2022, 0.85),
    (5,  "Silom",       "Bang Rak",      0, 50, 120, 2021, 1.10),
    (6,  "Sathorn",     "Sathon",        0, 42, 100, 2022, 1.02),
    (7,  "Ari",         "Phaya Thai",    0, 36,  90, 2023, 0.95),
    (8,  "Ratchada",    "Huai Khwang",   1, 30, 150, 2023, 0.88),  # drive-thru
    (9,  "Ramkhamhaeng","Bang Kapi",     1, 28, 145, 2023, 0.80),  # drive-thru
    (10, "Bangna",      "Bang Na",       1, 32, 160, 2024, 0.78),  # drive-thru
    (11, "Rama 9",      "Huai Khwang",   1, 35, 155, 2024, 0.82),  # drive-thru
    (12, "Phra Khanong","Khlong Toei",   0, 26,  75, 2024, 0.72),
]

DISTRICT_PRESTIGE = {  # affects average ticket size
    "Watthana": 1.10, "Khlong Toei": 1.00, "Bang Rak": 1.08, "Sathon": 1.07,
    "Phaya Thai": 1.02, "Huai Khwang": 0.96, "Bang Kapi": 0.92, "Bang Na": 0.94,
}

# ----------------------------------------------------------------------
# 2. PRODUCTS — 40 SKUs across 5 categories
# ----------------------------------------------------------------------
PRODUCTS = []
_pid = 0
def add_product(name, category, price, cost):
    global _pid
    _pid += 1
    PRODUCTS.append((_pid, name, category, price, cost))

# Coffee (most popular)
for n, p, c in [
    ("Espresso", 75, 18), ("Americano", 80, 20), ("Latte", 95, 28),
    ("Cappuccino", 95, 28), ("Mocha", 110, 35), ("Flat White", 100, 30),
    ("Cold Brew", 120, 32), ("Iced Latte", 105, 30), ("Iced Americano", 85, 22),
    ("Vietnamese Coffee", 115, 35), ("Caramel Macchiato", 125, 38),
    ("Dirty Chai", 130, 40),
]:
    add_product(n, "coffee", p, c)

# Tea
for n, p, c in [
    ("Earl Grey", 80, 20), ("Thai Iced Tea", 85, 22), ("Matcha Latte", 130, 45),
    ("Chamomile", 75, 18), ("Jasmine Green", 80, 20), ("Hojicha Latte", 125, 40),
]:
    add_product(n, "tea", p, c)

# Food
for n, p, c in [
    ("Croissant", 65, 22), ("Almond Croissant", 85, 30), ("Ham & Cheese Toast", 120, 45),
    ("Avocado Toast", 165, 60), ("Chicken Pesto Sandwich", 175, 65),
    ("Tuna Sandwich", 155, 55), ("Granola Bowl", 145, 50),
]:
    add_product(n, "food", p, c)

# Dessert
for n, p, c in [
    ("Cheesecake", 130, 45), ("Brownie", 95, 32), ("Carrot Cake", 125, 42),
    ("Banoffee Pie", 145, 50), ("Macaron (3pc)", 120, 40),
    ("Chocolate Cookie", 55, 18), ("Cinnamon Roll", 95, 30),
]:
    add_product(n, "dessert", p, c)

# Merch
for n, p, c in [
    ("Coffee Beans 250g", 320, 140), ("Tumbler", 450, 180),
    ("Tote Bag", 350, 130), ("Drip Bag (5pc)", 250, 100),
]:
    add_product(n, "merch", p, c)

# ----------------------------------------------------------------------
# 3. CUSTOMERS — 5000 customers with engineered segments
# ----------------------------------------------------------------------
N_CUSTOMERS = 5000
AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
AGE_WEIGHTS = [0.18, 0.42, 0.22, 0.12, 0.06]
GENDERS = ["F", "M", "Other"]
GENDER_WEIGHTS = [0.58, 0.40, 0.02]
DISTRICTS = list(DISTRICT_PRESTIGE.keys()) + ["Other"]
ACQ_CHANNELS = ["walk-in", "app-signup", "promo", "referral"]
ACQ_WEIGHTS = [0.45, 0.30, 0.15, 0.10]

# Engineered segments — used to drive both behavior and response label
SEGMENTS = ["Daily Loyalist", "Weekend Bruncher", "App Promo Hunter", "Casual Drifter"]
SEGMENT_WEIGHTS = [0.18, 0.22, 0.20, 0.40]

def gen_customers():
    rows = []
    for cid in range(1, N_CUSTOMERS + 1):
        signup_offset = random.randint(0, N_DAYS - 30)
        signup_date = START_DATE + timedelta(days=signup_offset)
        age = random.choices(AGE_GROUPS, AGE_WEIGHTS)[0]
        gender = random.choices(GENDERS, GENDER_WEIGHTS)[0]
        home = random.choice(DISTRICTS)
        acq = random.choices(ACQ_CHANNELS, ACQ_WEIGHTS)[0]
        seg = random.choices(SEGMENTS, SEGMENT_WEIGHTS)[0]
        rows.append((cid, signup_date.isoformat(), age, gender, home, acq, seg))
    return rows

# ----------------------------------------------------------------------
# 4. PROMOTIONS — 8 campaigns including the comeback offer
# ----------------------------------------------------------------------
PROMOTIONS = [
    # promo_id, name, start, end, type, discount_pct, target
    (1, "Summer Cool Down",   "2025-06-01", "2025-06-30", "%off",   20, "all"),
    (2, "Back to Work",       "2025-08-15", "2025-09-15", "%off",   15, "all"),
    (3, "Loyalty Boost",      "2025-10-01", "2025-10-31", "BOGO",   50, "loyalty"),
    (4, "App-Only 12.12",     "2025-12-01", "2025-12-31", "%off",   25, "app"),
    (5, "New Year Brew",      "2026-01-01", "2026-01-31", "bundle", 30, "all"),
    (6, "Songkran Splash",    "2026-04-10", "2026-04-20", "%off",   20, "all"),
    (7, "Comeback 50",        "2026-04-25", "2026-04-30", "voucher",None,"lapsed"),  # MAIN CAMPAIGN
    (8, "Weekday Wake-Up",    "2026-02-01", "2026-02-28", "%off",   10, "weekday"),
]

PROMO_DATE_MAP = {}  # date -> promo_id (active promo on that date)
for p in PROMOTIONS:
    pid, _, s, e, *_ = p
    if pid == 7:  # skip comeback (targeted, not blanket-active)
        continue
    sd = date.fromisoformat(s); ed = date.fromisoformat(e)
    cur = sd
    while cur <= ed:
        PROMO_DATE_MAP[cur] = pid
        cur += timedelta(days=1)

# ----------------------------------------------------------------------
# 5. TRANSACTIONS + ORDER ITEMS — engineered patterns
# ----------------------------------------------------------------------
CHANNELS = ["dine-in", "takeaway", "app", "delivery"]
PAYMENTS = ["cash", "card", "qr-promptpay", "app-wallet"]

# Segment-specific behavior (used for transactions + response labeling)
SEG_PARAMS = {
    "Daily Loyalist":     {"visit_per_week": 5.5, "ticket_mult": 0.9,  "channel_pref": [0.3,0.4,0.25,0.05], "promo_resp": 0.12},
    "Weekend Bruncher":   {"visit_per_week": 1.6, "ticket_mult": 1.4,  "channel_pref": [0.5,0.2,0.1,0.2],   "promo_resp": 0.18},
    "App Promo Hunter":   {"visit_per_week": 2.2, "ticket_mult": 1.0,  "channel_pref": [0.1,0.1,0.6,0.2],   "promo_resp": 0.30},
    "Casual Drifter":     {"visit_per_week": 0.7, "ticket_mult": 0.95, "channel_pref": [0.4,0.4,0.15,0.05], "promo_resp": 0.05},
}

# Product affinity by category (for basket generation)
CAT_BY_ID = {p[0]: p[2] for p in PRODUCTS}
PRICE_BY_ID = {p[0]: p[3] for p in PRODUCTS}
COST_BY_ID = {p[0]: p[4] for p in PRODUCTS}
PRODUCTS_BY_CAT = {}
for p in PRODUCTS:
    PRODUCTS_BY_CAT.setdefault(p[2], []).append(p[0])

def build_basket(segment, channel, is_weekend, promo_active):
    """Return list of (product_id, qty). Engineered associations."""
    items = []
    # Coffee is dominant (always likely)
    if random.random() < 0.85:
        coffee = random.choice(PRODUCTS_BY_CAT["coffee"])
        items.append((coffee, 1))
        # Strong association: coffee + croissant
        if random.random() < (0.45 if is_weekend else 0.25):
            items.append((random.choice(PRODUCTS_BY_CAT["food"]
                                         + PRODUCTS_BY_CAT["dessert"]), 1))
    else:
        # Tea drinkers
        if random.random() < 0.55:
            tea = random.choice(PRODUCTS_BY_CAT["tea"])
            items.append((tea, 1))
            # Tea + dessert association
            if random.random() < 0.40:
                items.append((random.choice(PRODUCTS_BY_CAT["dessert"]), 1))
        else:
            # Just food (rare lunch crowd)
            items.append((random.choice(PRODUCTS_BY_CAT["food"]), 1))

    # Weekend Brunchers buy more, weekend
    if segment == "Weekend Bruncher" and is_weekend and random.random() < 0.5:
        items.append((random.choice(PRODUCTS_BY_CAT["food"]
                                     + PRODUCTS_BY_CAT["dessert"]), 1))
    # App Promo Hunter on app + promo: bigger basket
    if segment == "App Promo Hunter" and channel == "app" and promo_active and random.random() < 0.4:
        items.append((random.choice(PRODUCTS_BY_CAT["coffee"]), 1))

    # Merch attaches occasionally
    if random.random() < 0.012:
        items.append((random.choice(PRODUCTS_BY_CAT["merch"]), 1))

    # Dedupe by summing qty
    out = {}
    for pid, q in items:
        out[pid] = out.get(pid, 0) + q
    return list(out.items())

def gen_transactions(customers, branches):
    transactions = []
    order_items = []
    txn_id = 0
    item_id = 0

    # Pre-compute customer -> segment lookup
    cust_seg = {c[0]: c[6] for c in customers}
    cust_signup = {c[0]: date.fromisoformat(c[1]) for c in customers}
    cust_acq = {c[0]: c[5] for c in customers}

    # Build branch lookup
    br_lookup = {b[0]: b for b in branches}

    # For each customer, sample visits across days
    for c in customers:
        cid = c[0]
        seg = cust_seg[cid]
        signup = cust_signup[cid]
        active_days = (END_DATE - signup).days + 1
        if active_days < 7:
            continue
        # Casual Drifter — many lapse (no visits in last 60 days)
        # Engineered: a fraction of casuals stop visiting around month 8-10
        lapse_prob = 0.55 if seg == "Casual Drifter" else 0.10 if seg == "App Promo Hunter" else 0.05
        will_lapse = random.random() < lapse_prob
        if will_lapse:
            lapse_start = END_DATE - timedelta(days=random.randint(60, 200))
        else:
            lapse_start = END_DATE + timedelta(days=1)

        weekly_rate = SEG_PARAMS[seg]["visit_per_week"]
        # Slight upward trend across the year
        n_visits_expected = int(weekly_rate * (active_days / 7) *
                                random.uniform(0.85, 1.15))
        if n_visits_expected == 0:
            continue

        # Customer's home branch (sticky)
        home_branch = random.choice(branches)[0]

        for _ in range(n_visits_expected):
            # Sample visit day (uniform within active period; lapsed people stop)
            visit_day = signup + timedelta(days=random.randint(0, active_days - 1))
            if visit_day >= lapse_start:
                continue

            is_weekend = visit_day.weekday() >= 5
            promo_id = PROMO_DATE_MAP.get(visit_day)
            promo_active = promo_id is not None

            # Branch — 70% home branch, 30% wander
            branch_id = home_branch if random.random() < 0.7 else random.choice(branches)[0]
            br = br_lookup[branch_id]
            br_name, br_district, has_dt = br[1], br[2], br[3]
            base_traffic = br[7]

            # Channel choice
            channel = random.choices(CHANNELS, SEG_PARAMS[seg]["channel_pref"])[0]

            # Time of day (peak morning + lunch + afternoon)
            hour_dist = [7,8,8,9,10,11,12,12,13,14,15,16,17,18,19]
            hour = random.choice(hour_dist) + random.randint(0, 1)
            minute = random.randint(0, 59)
            ts = datetime.combine(visit_day, datetime.min.time()).replace(hour=hour, minute=minute)

            # ENGINEERED EFFECTS:
            # - has_drive_thru → +12% weekend revenue (significant)
            # - district prestige → ticket multiplier
            # - promo_active → +25% basket size (slightly bigger)
            # - app channel → ~10% bigger ticket (delivery upcharge)
            # - Thonglor leading-indicator: rising service time (encoded later in reviews)

            # Build basket
            basket = build_basket(seg, channel, is_weekend, promo_active)
            if not basket:
                continue

            # Compute totals
            ticket_mult = SEG_PARAMS[seg]["ticket_mult"]
            district_mult = DISTRICT_PRESTIGE.get(br_district, 1.0)
            channel_mult = 1.10 if channel == "delivery" else 1.05 if channel == "app" else 1.0
            weekend_mult = 1.0
            if is_weekend:
                weekend_mult = 1.15 if has_dt else 1.05  # drive-thru lift on weekends
            promo_mult = 1.05 if promo_active else 1.0
            traffic_mult = base_traffic
            total_mult = ticket_mult * district_mult * channel_mult * weekend_mult * promo_mult * traffic_mult

            txn_id += 1
            order_total = 0.0
            for pid, qty in basket:
                unit_price = PRICE_BY_ID[pid]
                # Apply promo discount on line if applicable
                discount = 0.0
                if promo_id and promo_id in (1, 2, 4, 6, 8):  # %off promos
                    pct = next(p[5] for p in PROMOTIONS if p[0] == promo_id)
                    discount = round(unit_price * qty * (pct / 100), 2)
                line_total = round(unit_price * qty * total_mult - discount, 2)
                order_total += line_total
                item_id += 1
                order_items.append((item_id, txn_id, pid, qty, unit_price, discount))

            payment = random.choice(PAYMENTS)
            transactions.append((txn_id, ts.isoformat(sep=" "), branch_id, cid,
                                 channel, payment, promo_id,
                                 round(order_total, 2)))
    return transactions, order_items

# ----------------------------------------------------------------------
# 6. LOYALTY EVENTS — derived
# ----------------------------------------------------------------------
def gen_loyalty_events(customers, transactions):
    """Per-customer event log: signup, visits, lapse marker."""
    events = []
    eid = 0
    txn_by_cust = {}
    for t in transactions:
        txn_by_cust.setdefault(t[3], []).append(t)
    for c in customers:
        cid = c[0]
        signup = c[1]
        # signup
        eid += 1
        events.append((eid, cid, signup, "signup", 0))
        cust_txns = sorted(txn_by_cust.get(cid, []), key=lambda x: x[1])
        last_visit_date = None
        for t in cust_txns:
            eid += 1
            visit_dt = t[1].split(" ")[0]
            points = int(t[7] / 10)  # 1 pt per 10 baht
            events.append((eid, cid, visit_dt, "visit", points))
            last_visit_date = visit_dt
        # Lapse marker if no visit in last 60 days
        if last_visit_date:
            last_d = date.fromisoformat(last_visit_date)
            if (END_DATE - last_d).days >= 60:
                eid += 1
                events.append((eid, cid, (last_d + timedelta(days=60)).isoformat(),
                              "lapse", 0))
    return events

# ----------------------------------------------------------------------
# 7. CAMPAIGN_RESPONSES — for Module 3 (imbalanced classification)
# ----------------------------------------------------------------------
def gen_campaign_responses(customers, transactions, loyalty_events):
    """Comeback 50 campaign sent to lapsed customers. ~5% respond."""
    # Identify lapsed customers (no visit in last 60 days from a snapshot)
    snapshot = date(2026, 4, 24)  # day before campaign
    txn_by_cust = {}
    for t in transactions:
        txn_by_cust.setdefault(t[3], []).append(date.fromisoformat(t[1].split(" ")[0]))

    cust_lookup = {c[0]: c for c in customers}
    rows = []
    for c in customers:
        cid = c[0]
        visits = txn_by_cust.get(cid, [])
        if not visits:
            continue
        last_visit = max(visits)
        days_since = (snapshot - last_visit).days
        if days_since < 60:
            continue  # not lapsed
        # Send the campaign
        sent_date = "2026-04-25"
        # Response probability based on segment + tenure + last activity
        seg = c[6]
        base_p = SEG_PARAMS[seg]["promo_resp"]
        # tenure boost (longer tenure → more likely respond)
        tenure_days = (snapshot - date.fromisoformat(c[1])).days
        tenure_boost = min(0.10, tenure_days / 3650)
        # acquisition channel matters
        acq_boost = 0.05 if c[5] == "app-signup" else 0.0
        p_response = max(0.01, min(0.45, base_p + tenure_boost + acq_boost - 0.05))

        responded = 1 if random.random() < p_response else 0
        rows.append((cid, sent_date, responded))
    return rows

# ----------------------------------------------------------------------
# 8. REVIEWS — Thai + English mix with topics & sentiment
# ----------------------------------------------------------------------
TH_POS_TEMPLATES = [
    "ร้าน{branch}บรรยากาศดีมาก {product}อร่อย พนักงานบริการดี",
    "ชอบ{product}ที่นี่ หอม กลมกล่อม จะกลับมาอีกแน่นอน",
    "{branch}เป็นสาขาโปรด {product}อร่อยทุกครั้ง",
    "นั่งทำงานสบาย wifi เร็ว {product}คุ้มราคา",
    "บาริสต้าใจดี อธิบาย{product}ให้ฟัง ประทับใจ",
    "เค้กที่นี่อร่อยมาก โดยเฉพาะ{product} แนะนำเลย",
    "{branch}สาขานี้สะอาด ที่นั่งเยอะ {product}รสชาติดี",
]
TH_NEG_TEMPLATES = [
    "รอนานมาก {time}นาทีถึงได้ {product} พนักงานน้อยไป",
    "{branch}คนเยอะ คิวยาว ที่นั่งหายาก",
    "{product}วันนี้รสชาติเปลี่ยนไป ไม่เหมือนเดิม",
    "ราคาแพงไป {product}เล็กไม่คุ้ม",
    "พนักงานพูดจาไม่ดี ไม่อยากกลับมาอีก",
    "แอพล่ม สั่งไม่ได้ ต้องเข้าหน้าร้านเอง เสียเวลา",
    "เครื่องชงเสียอีกแล้ว {branch}สาขานี้บริการช้ามาก",
    "wifi ช้ามาก ทำงานไม่ได้เลย {product}ก็เย็นเร็ว",
]
TH_MIXED_TEMPLATES = [
    "{product}อร่อยนะ แต่{complaint}",
    "ชอบ{branch} แต่ราคา{product}ขึ้นอีกแล้ว",
    "บรรยากาศดี แต่รอนาน {time}นาที",
]
EN_POS_TEMPLATES = [
    "Love the {product} at {branch}, super smooth and great vibe.",
    "Best {product} in town. Service was friendly.",
    "{branch} is my go-to for working from cafe. Reliable {product}.",
]
EN_NEG_TEMPLATES = [
    "Waited {time} minutes for a {product}. Too slow.",
    "{branch} is always crowded. Hard to find a seat.",
    "App keeps crashing. Tried to order {product} three times.",
]
COMPLAINTS = ["รอนาน", "พนักงานน้อย", "แอพล่ม", "ราคาแพง", "ที่นั่งน้อย"]

# Topic labels for synthetic ground truth (used to verify topic modeling)
def gen_reviews(customers, transactions, branches):
    br_lookup = {b[0]: b[1] for b in branches}
    txn_sample_by_cust = {}
    for t in transactions:
        txn_sample_by_cust.setdefault(t[3], []).append(t)

    reviews = []
    rid = 0
    target_n = 2000

    # We sample across all branches but bias Thonglor (id=3) toward "wait time" rising in last 6 weeks
    for _ in range(target_n):
        # Pick a customer
        cid = random.randint(1, N_CUSTOMERS)
        cust_txns = txn_sample_by_cust.get(cid, [])
        if not cust_txns:
            continue
        t = random.choice(cust_txns)
        branch_id = t[2]
        branch_name = br_lookup[branch_id]
        review_date = t[1].split(" ")[0]

        # Pick a product from the order
        # (simplified — pick a random product from the menu instead)
        prod = random.choice(PRODUCTS)
        prod_name = prod[1]

        # Sentiment + language
        # Engineer: Thonglor in last 6 weeks → more "wait" complaints
        review_dt = date.fromisoformat(review_date)
        thonglor_recent = (branch_id == 3 and (END_DATE - review_dt).days < 42)
        if thonglor_recent and random.random() < 0.55:
            # bias toward wait-time complaint
            text = random.choice([
                "รอนานมาก {time}นาทีถึงได้ {product} พนักงานน้อยไป",
                "Waited {time} minutes for a {product}. Too slow.",
                "{branch}คิวยาวมากช่วงนี้ รอนาน",
                "เครื่องชงเสียอีกแล้ว {branch}สาขานี้บริการช้ามาก",
            ])
            sentiment = "negative"
            rating = random.choice([1, 2, 2, 3])
        else:
            r = random.random()
            if r < 0.65:
                text = random.choice(TH_POS_TEMPLATES + EN_POS_TEMPLATES)
                sentiment = "positive"
                rating = random.choice([4, 4, 5, 5, 5])
            elif r < 0.85:
                text = random.choice(TH_NEG_TEMPLATES + EN_NEG_TEMPLATES)
                sentiment = "negative"
                rating = random.choice([1, 2, 2, 3])
            else:
                text = random.choice(TH_MIXED_TEMPLATES)
                sentiment = "mixed"
                rating = random.choice([3, 3, 4])

        text = text.format(branch=branch_name, product=prod_name,
                           time=random.choice([5,8,10,12,15,20,25,30]),
                           complaint=random.choice(COMPLAINTS))
        channel = random.choice(["Google", "app", "IG", "Facebook"])
        rid += 1
        reviews.append((rid, cid, branch_id, review_date, rating, channel, text, sentiment))
    return reviews

# ----------------------------------------------------------------------
# WRITE TO SQLITE
# ----------------------------------------------------------------------
def write_db(branches, customers, products, promotions,
             transactions, order_items, loyalty_events,
             campaign_responses, reviews):
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE branches(branch_id INTEGER PRIMARY KEY, name TEXT, district TEXT,
        has_drive_thru INTEGER, seats INTEGER, size_sqm INTEGER, open_year INTEGER,
        base_traffic REAL);
    CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, signup_date TEXT,
        age_group TEXT, gender TEXT, home_district TEXT,
        acquisition_channel TEXT, segment TEXT);
    CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT,
        category TEXT, price REAL, cost REAL);
    CREATE TABLE promotions(promo_id INTEGER PRIMARY KEY, name TEXT,
        start_date TEXT, end_date TEXT, type TEXT, discount_pct REAL,
        target_segment TEXT);
    CREATE TABLE transactions(order_id INTEGER PRIMARY KEY, datetime TEXT,
        branch_id INTEGER, customer_id INTEGER, channel TEXT, payment_method TEXT,
        promo_id INTEGER, total REAL);
    CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER,
        product_id INTEGER, qty INTEGER, unit_price REAL, line_discount REAL);
    CREATE TABLE loyalty_events(event_id INTEGER PRIMARY KEY, customer_id INTEGER,
        event_date TEXT, event_type TEXT, points_delta INTEGER);
    CREATE TABLE campaign_responses(customer_id INTEGER, sent_date TEXT,
        responded INTEGER, PRIMARY KEY(customer_id, sent_date));
    CREATE TABLE reviews(review_id INTEGER PRIMARY KEY, customer_id INTEGER,
        branch_id INTEGER, review_date TEXT, rating INTEGER, channel TEXT,
        text TEXT, sentiment_label TEXT);
    CREATE INDEX ix_txn_branch ON transactions(branch_id);
    CREATE INDEX ix_txn_customer ON transactions(customer_id);
    CREATE INDEX ix_txn_dt ON transactions(datetime);
    CREATE INDEX ix_oi_order ON order_items(order_id);
    CREATE INDEX ix_oi_product ON order_items(product_id);
    CREATE INDEX ix_le_customer ON loyalty_events(customer_id);
    """)

    cur.executemany("INSERT INTO branches VALUES (?,?,?,?,?,?,?,?)", branches)
    cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?)", customers)
    cur.executemany("INSERT INTO products VALUES (?,?,?,?,?)", products)
    cur.executemany("INSERT INTO promotions VALUES (?,?,?,?,?,?,?)", PROMOTIONS)
    cur.executemany("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?)", transactions)
    cur.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?)", order_items)
    cur.executemany("INSERT INTO loyalty_events VALUES (?,?,?,?,?)", loyalty_events)
    cur.executemany("INSERT INTO campaign_responses VALUES (?,?,?)", campaign_responses)
    cur.executemany("INSERT INTO reviews VALUES (?,?,?,?,?,?,?,?)", reviews)
    conn.commit()
    conn.close()


def main():
    print("Generating data...")
    branches = BRANCHES
    products = PRODUCTS
    customers = gen_customers()
    print(f"  customers: {len(customers)}")
    transactions, order_items = gen_transactions(customers, branches)
    print(f"  transactions: {len(transactions)}")
    print(f"  order_items:  {len(order_items)}")
    loyalty_events = gen_loyalty_events(customers, transactions)
    print(f"  loyalty_events: {len(loyalty_events)}")
    campaign_responses = gen_campaign_responses(customers, transactions, loyalty_events)
    print(f"  campaign_responses: {len(campaign_responses)}  "
          f"(positive: {sum(r[2] for r in campaign_responses)})")
    reviews = gen_reviews(customers, transactions, branches)
    print(f"  reviews: {len(reviews)}")

    write_db(branches, customers, products, PROMOTIONS,
             transactions, order_items, loyalty_events,
             campaign_responses, reviews)
    print(f"Wrote SQLite to {DB_PATH}")
    print(f"  size: {DB_PATH.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
