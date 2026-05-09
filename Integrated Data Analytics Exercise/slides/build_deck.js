// MADT6004 Wrap-Up Session — Integrated Data Analytics Exercise
// Brew Lab BKK case
// MADT teal style: #0891B2 primary, Arial, 16:9, white content + dark dividers

process.env.NODE_PATH = '/home/claude/.npm-global/lib/node_modules';
require('module').Module._initPaths();
const pptxgen = require('pptxgenjs');

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";  // 13.33 x 7.5
pres.defineLayout({ name: "MADT_16x9", width: 10, height: 5.625 });
pres.layout = "MADT_16x9";

// Color palette
const C = {
  teal: "0891B2",
  teal_light: "E0F7FA",
  dark: "1F2937",
  body: "374151",
  med: "6B7280",
  light: "9CA3AF",
  card: "F3F4F6",
  amber: "D97706",
  amber_bg: "FEF3C7",
  green: "059669",
  red: "DC2626",
  purple: "6D28D9",
  divider: "D1D5DB",
  white: "FFFFFF",
};

const F = "Arial";
const FOOTER_TEXT = "NIDA  |  MADT6004";

// ============ HELPERS ============

function addTopBar(slide) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.05, fill: { color: C.teal }, line: { type: "none" }
  });
}

function addFooter(slide, section) {
  slide.addText(`${FOOTER_TEXT}  |  ${section}`, {
    x: 0.7, y: 5.28, w: 6, h: 0.25,
    fontSize: 9, fontFace: F, color: C.light, margin: 0
  });
  slide.addText("MADT", {
    x: 8.5, y: 5.25, w: 1.0, h: 0.3,
    fontSize: 12, fontFace: F, bold: true, color: C.teal,
    align: "right", margin: 0
  });
}

function contentSlide(section) {
  const slide = pres.addSlide();
  slide.background = { color: C.white };
  addTopBar(slide);
  addFooter(slide, section);
  return slide;
}

function addTitle(slide, title, subtitle) {
  slide.addText(title, {
    x: 0.7, y: 0.3, w: 8.6, h: 0.55,
    fontSize: 28, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.7, y: 0.85, w: 8.6, h: 0.3,
      fontSize: 13, fontFace: F, color: C.med, italic: true, margin: 0
    });
  }
}

function dividerSlide(num, title, subtitle) {
  const slide = pres.addSlide();
  slide.background = { color: C.dark };
  addTopBar(slide);

  slide.addText(num, {
    x: 0.7, y: 1.3, w: 2.5, h: 1.4,
    fontSize: 80, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  slide.addShape(pres.shapes.LINE, {
    x: 0.7, y: 2.85, w: 3.5, h: 0,
    line: { color: C.teal, width: 2.5 }
  });
  slide.addText(title, {
    x: 0.7, y: 3.05, w: 8.6, h: 0.7,
    fontSize: 36, fontFace: F, bold: true, color: C.white, margin: 0
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.7, y: 3.85, w: 8.6, h: 0.5,
      fontSize: 16, fontFace: F, color: C.light, italic: true, margin: 0
    });
  }
  slide.addText("MADT", {
    x: 8.4, y: 0.25, w: 1.2, h: 0.4,
    fontSize: 13, fontFace: F, bold: true, color: C.teal, align: "right"
  });
  return slide;
}

function card(slide, x, y, w, h, accentColor, title, body) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: C.card }, line: { color: C.divider, width: 0.5 }
  });
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.07, h, fill: { color: accentColor }, line: { type: "none" }
  });
  slide.addText(title, {
    x: x + 0.2, y: y + 0.1, w: w - 0.3, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  slide.addText(body, {
    x: x + 0.2, y: y + 0.5, w: w - 0.3, h: h - 0.6,
    fontSize: 11, fontFace: F, color: C.body, margin: 0, valign: "top"
  });
}

function calloutBox(slide, x, y, w, h, text, kind) {
  const fill = kind === "warn" ? C.amber_bg : C.teal_light;
  const accent = kind === "warn" ? C.amber : C.teal;
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill }, line: { color: accent, width: 1 }
  });
  slide.addText(text, {
    x: x + 0.2, y: y + 0.1, w: w - 0.4, h: h - 0.2,
    fontSize: 12, fontFace: F, color: C.dark, italic: true, margin: 0,
    valign: "middle"
  });
}

function codeBlock(slide, x, y, w, h, code, fontSize) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: C.card }, line: { color: C.divider, width: 0.5 }
  });
  slide.addText(code, {
    x: x + 0.15, y: y + 0.1, w: w - 0.3, h: h - 0.2,
    fontSize: fontSize || 10, fontFace: "Consolas", color: C.body,
    valign: "top", margin: 0
  });
}

// ============ SLIDE 1: TITLE ============
{
  const slide = pres.addSlide();
  slide.background = { color: C.dark };
  addTopBar(slide);

  slide.addText("MADT", {
    x: 8.4, y: 0.25, w: 1.2, h: 0.4,
    fontSize: 13, fontFace: F, bold: true, color: C.teal, align: "right"
  });

  slide.addText("Wrap-Up Session", {
    x: 0.7, y: 1.4, w: 8.6, h: 0.4,
    fontSize: 14, fontFace: F, color: C.light, margin: 0
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 1.95, w: 0.08, h: 1.7,
    fill: { color: C.teal }, line: { type: "none" }
  });

  slide.addText("Integrated Data Analytics Exercise", {
    x: 0.95, y: 1.9, w: 8.4, h: 1.0,
    fontSize: 40, fontFace: F, bold: true, color: C.white, margin: 0
  });

  slide.addText("Five modules. One coffee chain. The full journey from raw data to defensible decisions.", {
    x: 0.95, y: 3.0, w: 8.4, h: 0.6,
    fontSize: 16, fontFace: F, color: C.light, italic: true, margin: 0
  });

  slide.addText("MADT6004  |  Applied Data Analytics for Business", {
    x: 0.7, y: 4.4, w: 8.6, h: 0.3,
    fontSize: 12, fontFace: F, color: C.light, margin: 0
  });
  slide.addText("Asst. Prof. Dr. Thanachart Ritbumroong  |  NIDA", {
    x: 0.7, y: 4.7, w: 8.6, h: 0.3,
    fontSize: 12, fontFace: F, color: C.light, margin: 0
  });
}

// ============ SLIDE 2: THE CASE ============
{
  const s = contentSlide("Setup");
  addTitle(s, "Brew Lab BKK", "12-branch specialty coffee chain across Bangkok");

  // Stats row
  const stats = [
    { num: "12", lbl: "branches" },
    { num: "5K", lbl: "loyalty members" },
    { num: "267K", lbl: "transactions" },
    { num: "1.8K", lbl: "customer reviews" },
    { num: "12mo", lbl: "of history" },
  ];
  stats.forEach((st, i) => {
    const x = 0.7 + i * 1.78;
    s.addText(st.num, {
      x: x, y: 1.4, w: 1.6, h: 0.7,
      fontSize: 36, fontFace: F, bold: true, color: C.teal, align: "center", margin: 0
    });
    s.addText(st.lbl, {
      x: x, y: 2.05, w: 1.6, h: 0.3,
      fontSize: 11, fontFace: F, color: C.med, align: "center", margin: 0
    });
  });

  // Description
  s.addText("All branches sit in central Bangkok. Four are drive-thrus on outer roads; eight are walk-in shops in higher-prestige districts. Mixed channel mix: dine-in, takeaway, app, delivery. ~60K loyalty signups; 12 months of clean transaction history through April 2026.", {
    x: 0.7, y: 2.7, w: 8.6, h: 1.0,
    fontSize: 13, fontFace: F, color: C.body, margin: 0, valign: "top"
  });

  calloutBox(s, 0.7, 4.0, 8.6, 0.85,
    "The case is fictional. The patterns are real — engineered to surface signal in every module. What you find today, you will find at every Thai retail client.",
    "tip");
}

// ============ SLIDE 3: THE FIVE QUESTIONS ============
{
  const s = contentSlide("The questions");
  addTitle(s, "Khun Ploy's five questions", "The COO doesn't want models. She wants answers.");

  const qs = [
    { n: "01", q: "What actually drives daily branch revenue?", who: "Strategy" },
    { n: "02", q: "How much will each SKU sell at each branch over the next 30 days?", who: "Operations" },
    { n: "03", q: "Of the next batch of lapsed members, who will respond to the comeback voucher?", who: "Marketing" },
    { n: "04", q: "How many real types of customer do we have, and what should we put in front of them?", who: "Product" },
    { n: "05", q: "What are customers actually saying — and where is it worst?", who: "Service" },
  ];
  qs.forEach((qq, i) => {
    const y = 1.4 + i * 0.75;
    s.addText(qq.n, {
      x: 0.7, y, w: 0.7, h: 0.6,
      fontSize: 24, fontFace: F, bold: true, color: C.teal, margin: 0
    });
    s.addText(qq.q, {
      x: 1.45, y: y + 0.1, w: 6.4, h: 0.6,
      fontSize: 13, fontFace: F, color: C.dark, bold: true,
      valign: "middle", margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x: 8.0, y: y + 0.05, w: 1.3, h: 0.45,
      fill: { color: C.teal_light }, line: { color: C.teal, width: 0.5 }
    });
    s.addText(qq.who, {
      x: 8.0, y: y + 0.05, w: 1.3, h: 0.45,
      fontSize: 10, fontFace: F, color: C.teal, bold: true, align: "center", valign: "middle", margin: 0
    });
  });
}

// ============ SLIDE 4: TODAY'S JOURNEY ============
{
  const s = contentSlide("Today");
  addTitle(s, "Today's journey", "Five modules. One thread. Three hours.");

  const acts = [
    { n: "01", title: "Diagnose", sub: "What's actually true",         color: C.teal,   t: "50 min" },
    { n: "02", title: "Forecast", sub: "What's coming",                color: C.green,  t: "55 min" },
    { n: "03", title: "Predict",  sub: "Who responds",                 color: C.amber,  t: "30 min" },
    { n: "04", title: "Segment",  sub: "Who they are + what to offer", color: C.purple, t: "30 min" },
    { n: "05", title: "Listen",   sub: "What they're saying",          color: C.red,    t: "25 min" },
  ];

  acts.forEach((a, i) => {
    const y = 1.4 + i * 0.7;
    // colored square with number
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0.7, y, w: 0.6, h: 0.6,
      fill: { color: a.color }, line: { type: "none" }
    });
    s.addText(a.n, {
      x: 0.7, y, w: 0.6, h: 0.6,
      fontSize: 18, fontFace: F, bold: true, color: C.white,
      align: "center", valign: "middle", margin: 0
    });
    s.addText(a.title, {
      x: 1.5, y, w: 2.5, h: 0.3,
      fontSize: 16, fontFace: F, bold: true, color: C.dark, margin: 0
    });
    s.addText(a.sub, {
      x: 1.5, y: y + 0.3, w: 5.5, h: 0.3,
      fontSize: 12, fontFace: F, color: C.med, italic: true, margin: 0
    });
    s.addText(a.t, {
      x: 8.5, y: y + 0.05, w: 0.9, h: 0.5,
      fontSize: 12, fontFace: F, color: C.light,
      align: "right", valign: "middle", margin: 0
    });
  });

  calloutBox(s, 0.7, 5.0, 8.6, 0.45,
    "By the end, Module 5 feeds back into Module 3, and Module 4 filters what we send. The loop closes.",
    "tip");
}

// ============ SLIDE 5: M1 DIVIDER ============
dividerSlide("01", "Diagnose", "What is actually driving daily branch revenue?");

// ============ SLIDE 6: M1 — THE TRAP ============
{
  const s = contentSlide("Module 1 — the trap");
  addTitle(s, "The trap of running many tests", "Run 30 t-tests, report the p<.05 ones, declare insight. This is not analysis.");

  // Two-column comparison
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 1.4, w: 4.1, h: 3.2,
    fill: { color: C.amber_bg }, line: { color: C.amber, width: 1 }
  });
  s.addText("WITHOUT discipline", {
    x: 0.85, y: 1.5, w: 3.8, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.amber, margin: 0
  });
  s.addText([
    { text: "•  Run every comparison you can think of\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Pick the ones with p < .05\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Tell a story around them\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Forget about multiple-comparisons inflation\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Confound categorical effects with continuous ones\n", options: { fontSize: 12, color: C.body } },
    { text: "\n", options: {} },
    { text: "Result: false positives, lost trust, wrong actions", options: { fontSize: 11, color: C.amber, bold: true, italic: true } },
  ], {
    x: 0.85, y: 1.95, w: 3.8, h: 2.5,
    fontFace: F, valign: "top", margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 1.4, w: 4.1, h: 3.2,
    fill: { color: C.teal_light }, line: { color: C.teal, width: 1 }
  });
  s.addText("WITH discipline", {
    x: 5.35, y: 1.5, w: 3.8, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  s.addText([
    { text: "•  Pre-register hypotheses as a dictionary\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Pick test by data type — automated\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Apply FDR (Benjamini-Hochberg) correction\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Confirm with regression + interactions\n", options: { fontSize: 12, color: C.body } },
    { text: "•  Filter to significant only → dashboard\n", options: { fontSize: 12, color: C.body } },
    { text: "\n", options: {} },
    { text: "Result: a defensible audit trail", options: { fontSize: 11, color: C.teal, bold: true, italic: true } },
  ], {
    x: 5.35, y: 1.95, w: 3.8, h: 2.5,
    fontFace: F, valign: "top", margin: 0
  });

  calloutBox(s, 0.7, 4.75, 8.6, 0.4,
    "The dictionary is the audit trail. Every reviewer can see what you tested — not just what worked.",
    "tip");
}

// ============ SLIDE 7: M1 — THE PATTERN ============
{
  const s = contentSlide("Module 1 — pattern");
  addTitle(s, "Causal chain as a dictionary", "Every relationship is a row in a table. No hidden tests.");

  codeBlock(s, 0.7, 1.3, 8.6, 3.0,
`CAUSAL_CHAIN = {
    "h01_dt_revenue":         {"cause":"has_drive_thru", "effect":"revenue",
                               "cause_type":"binary",     "effect_type":"continuous"},
    "h02_dt_weekend_revenue": {"cause":"has_drive_thru", "effect":"revenue",
                               "cause_type":"binary",     "effect_type":"continuous",
                               "subset":"is_weekend==1"},
    "h04_weekend_revenue":    {"cause":"is_weekend",     "effect":"revenue",
                               "cause_type":"binary",     "effect_type":"continuous"},
    "h07_seats_revenue":      {"cause":"seats",          "effect":"revenue",
                               "cause_type":"continuous", "effect_type":"continuous"},
    "h11_district_revenue":   {"cause":"district",       "effect":"revenue",
                               "cause_type":"categorical","effect_type":"continuous"},
    # ... 20 hypotheses total, all declared upfront
}`, 10);

  calloutBox(s, 0.7, 4.45, 8.6, 0.7,
    "The dictionary makes hypotheses first-class. You can version them. Diff them. Replay last quarter's analysis when the data changes.",
    "tip");
}

// ============ SLIDE 8: M1 — DISPATCH FUNCTION ============
{
  const s = contentSlide("Module 1 — dispatch");
  addTitle(s, "Pick the test by data type", "One function. Four type signatures. Uniform output.");

  // 4-row table
  const rows = [
    ["binary",       "continuous",  "Welch's t-test",      "Cohen's d"],
    ["categorical",  "continuous",  "One-way ANOVA",       "η² (eta-squared)"],
    ["continuous",   "continuous",  "Pearson correlation", "r"],
    ["categorical",  "categorical", "Chi-square",          "Cramer's V"],
  ];
  const colW = [1.5, 1.5, 2.6, 2.5];
  const xs = [0.7, 2.2, 3.7, 6.3];
  // header
  ["Cause type", "Effect type", "Test", "Effect-size measure"].forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: xs[i], y: 1.4, w: colW[i], h: 0.4,
      fill: { color: C.teal }, line: { type: "none" }
    });
    s.addText(h, {
      x: xs[i], y: 1.4, w: colW[i], h: 0.4,
      fontSize: 11, fontFace: F, bold: true, color: C.white,
      align: "center", valign: "middle", margin: 0
    });
  });
  rows.forEach((r, i) => {
    const y = 1.8 + i * 0.4;
    const fill = i % 2 === 0 ? C.white : C.card;
    r.forEach((cell, j) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x: xs[j], y, w: colW[j], h: 0.4,
        fill: { color: fill }, line: { color: C.divider, width: 0.5 }
      });
      s.addText(cell, {
        x: xs[j] + 0.05, y, w: colW[j] - 0.1, h: 0.4,
        fontSize: 11, fontFace: F, color: C.body,
        valign: "middle", margin: 0
      });
    });
  });

  s.addText("After the sweep:", {
    x: 0.7, y: 3.7, w: 8.6, h: 0.3,
    fontSize: 13, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  s.addText([
    { text: "1.  ", options: { color: C.teal, bold: true } },
    { text: "Apply Benjamini-Hochberg FDR correction across all p-values\n", options: {} },
    { text: "2.  ", options: { color: C.teal, bold: true } },
    { text: "Filter to q < 0.05 — those are your real findings\n", options: {} },
    { text: "3.  ", options: { color: C.teal, bold: true } },
    { text: "Confirm key effects with a regression that includes interactions\n", options: {} },
  ], {
    x: 0.7, y: 4.05, w: 8.6, h: 1.0,
    fontSize: 12, fontFace: F, color: C.body, valign: "top", margin: 0
  });
}

// ============ SLIDE 9: M1 — THE REVEAL ============
{
  const s = contentSlide("Module 1 — the reveal");
  addTitle(s, "The interaction reveal", "Naive and conditional answers can disagree. The regression is the tiebreaker.");

  // Two findings
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 1.3, w: 4.1, h: 1.6,
    fill: { color: C.amber_bg }, line: { color: C.amber, width: 1 }
  });
  s.addText("Naive t-test", {
    x: 0.85, y: 1.4, w: 3.8, h: 0.3,
    fontSize: 13, fontFace: F, bold: true, color: C.amber, margin: 0
  });
  s.addText("Drive-thru weekend revenue: 9,714 baht\nNon-drive-thru weekend revenue: 11,395 baht", {
    x: 0.85, y: 1.75, w: 3.8, h: 0.6,
    fontSize: 11, fontFace: F, color: C.body, margin: 0
  });
  s.addText("Conclusion: drive-thru is WORSE on weekends.", {
    x: 0.85, y: 2.4, w: 3.8, h: 0.4,
    fontSize: 12, fontFace: F, color: C.amber, italic: true, bold: true, margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 5.2, y: 1.3, w: 4.1, h: 1.6,
    fill: { color: C.teal_light }, line: { color: C.teal, width: 1 }
  });
  s.addText("Regression with interaction", {
    x: 5.35, y: 1.4, w: 3.8, h: 0.3,
    fontSize: 13, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  s.addText("revenue ~ has_drive_thru * is_weekend\n             + district + seats + size", {
    x: 5.35, y: 1.75, w: 3.8, h: 0.6,
    fontSize: 11, fontFace: F, color: C.body, margin: 0
  });
  s.addText("The interaction is positive and significant.\nDrive-thru weekend lift is LARGER, not smaller.", {
    x: 5.35, y: 2.35, w: 3.8, h: 0.5,
    fontSize: 12, fontFace: F, color: C.teal, italic: true, bold: true, margin: 0
  });

  s.addText("Why the disagreement?", {
    x: 0.7, y: 3.1, w: 8.6, h: 0.3,
    fontSize: 14, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  s.addText("Drive-thru branches sit in lower-prestige districts (Ratchada, Ramkhamhaeng, Bangna). Their absolute revenue is lower because of district, not because of weekend dynamics. Once you control for district, the drive-thru weekend lift emerges.", {
    x: 0.7, y: 3.45, w: 8.6, h: 1.0,
    fontSize: 12, fontFace: F, color: C.body, margin: 0, valign: "top"
  });

  calloutBox(s, 0.7, 4.55, 8.6, 0.55,
    "Lesson: a pairwise sweep tells you what's correlated. A regression with the right interactions tells you what's actually causal — given your controls.",
    "warn");
}

// ============ SLIDE 10: M2 DIVIDER ============
dividerSlide("02", "Forecast", "How much will each SKU sell at each branch?");

// ============ SLIDE 11: M2 — THE SHAPE ============
{
  const s = contentSlide("Module 2 — the shape");
  addTitle(s, "The forecasting panel", "Top 5 SKUs × 12 branches = 60 daily series");

  // Stats
  const stats = [
    { num: "60", lbl: "series to forecast" },
    { num: "365", lbl: "days of history (max)" },
    { num: "30", lbl: "days ahead horizon" },
    { num: "14", lbl: "days holdout for evaluation" },
  ];
  stats.forEach((st, i) => {
    const x = 0.7 + i * 2.22;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.4, w: 2.05, h: 1.1,
      fill: { color: C.card }, line: { color: C.divider, width: 0.5 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.4, w: 0.07, h: 1.1, fill: { color: C.teal }, line: { type: "none" }
    });
    s.addText(st.num, {
      x: x + 0.1, y: 1.5, w: 1.9, h: 0.55,
      fontSize: 32, fontFace: F, bold: true, color: C.teal, align: "center", margin: 0
    });
    s.addText(st.lbl, {
      x: x + 0.1, y: 2.05, w: 1.9, h: 0.4,
      fontSize: 10, fontFace: F, color: C.med, align: "center", margin: 0
    });
  });

  s.addText("Each series gets reindexed to a complete daily date range, zero-filled for missing days.", {
    x: 0.7, y: 2.75, w: 8.6, h: 0.3,
    fontSize: 12, fontFace: F, color: C.body, margin: 0
  });

  codeBlock(s, 0.7, 3.15, 8.6, 1.7,
`def make_series(daily, sku, branch):
    sub = daily[(daily.product_id == sku) & (daily.branch_id == branch)][['d', 'units']]
    sub = sub.set_index('d').sort_index()
    full_idx = pd.date_range(sub.index.min(), sub.index.max(), freq='D')
    return sub.reindex(full_idx, fill_value=0)['units']`, 11);
}

// ============ SLIDE 12: M2 — THE METHODS ============
{
  const s = contentSlide("Module 2 — methods");
  addTitle(s, "Three baselines worth knowing", "Always try the simple methods first.");

  const methods = [
    {
      title: "Naive",
      sub: "y_hat = last value",
      body: "Predict tomorrow = today, forever. Useless? Almost. But it's the floor your fancy models must beat.",
      color: C.amber,
    },
    {
      title: "Seasonal Naive",
      sub: "y_hat[t+h] = y[t+h-7]",
      body: "Predict same day-of-week from last week. Captures weekly seasonality — and surprisingly often wins.",
      color: C.teal,
    },
    {
      title: "Holt-Winters",
      sub: "trend + weekly seasonality, exponentially smoothed",
      body: "Adds level + trend + seasonal components. Earns its keep when SKUs have real upward/downward trends.",
      color: C.green,
    },
  ];

  methods.forEach((m, i) => {
    const x = 0.7 + i * 2.95;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.4, w: 2.7, h: 3.2,
      fill: { color: C.card }, line: { color: C.divider, width: 0.5 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.4, w: 2.7, h: 0.08,
      fill: { color: m.color }, line: { type: "none" }
    });
    s.addText(m.title, {
      x: x + 0.15, y: 1.55, w: 2.4, h: 0.4,
      fontSize: 18, fontFace: F, bold: true, color: C.dark, margin: 0
    });
    s.addText(m.sub, {
      x: x + 0.15, y: 1.95, w: 2.4, h: 0.4,
      fontSize: 11, fontFace: "Consolas", color: m.color, margin: 0
    });
    s.addText(m.body, {
      x: x + 0.15, y: 2.4, w: 2.4, h: 2.0,
      fontSize: 11, fontFace: F, color: C.body, valign: "top", margin: 0
    });
  });

  calloutBox(s, 0.7, 4.75, 8.6, 0.4,
    "RMSE is sensitive to large errors. If your business cares about steady misses, switch to MAE. The metric is a business choice, not a default.",
    "tip");
}

// ============ SLIDE 13: M2 — THE GRID ============
{
  const s = contentSlide("Module 2 — evaluation");
  addTitle(s, "Loop, evaluate, pick the winner per series", "60 series × 3 methods = 180 evaluations. Best method varies by SKU.");

  codeBlock(s, 0.7, 1.3, 8.6, 2.6,
`for sku in target_skus:
    for br in target_branches:
        s = make_series(daily, sku, br)
        train, test = s[:-14], s[-14:]
        for method, fn in {"naive": forecast_naive,
                           "seasonal_naive": forecast_seasonal_naive,
                           "holt_winters": forecast_holt_winters}.items():
            pred = fn(train, 14)
            records.append({"sku": sku, "branch": br, "method": method,
                            "rmse": rmse(test, pred)})`, 11);

  s.addText("What to look for in the results:", {
    x: 0.7, y: 4.05, w: 8.6, h: 0.3,
    fontSize: 13, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  s.addText([
    { text: "•  ", options: { color: C.teal, bold: true } },
    { text: "Seasonal naive often wins on small SKUs (low volume = noise dominates).\n", options: {} },
    { text: "•  ", options: { color: C.teal, bold: true } },
    { text: "Holt-Winters wins on high-volume SKUs with clear trend (e.g., Latte at Asoke).\n", options: {} },
    { text: "•  ", options: { color: C.teal, bold: true } },
    { text: "The heatmap of best-method RMSE is the operational artifact.\n", options: {} },
  ], {
    x: 0.7, y: 4.4, w: 8.6, h: 0.9,
    fontSize: 11, fontFace: F, color: C.body, valign: "top", margin: 0
  });
}

// ============ SLIDE 14: M3 DIVIDER ============
dividerSlide("03", "Predict", "Who will respond to the comeback voucher?");

// ============ SLIDE 15: M3 — THE IMBALANCE ============
{
  const s = contentSlide("Module 3 — imbalance");
  addTitle(s, "11% positive class", "Imbalanced enough to matter. Not so imbalanced that nothing trains.");

  // Big stat
  s.addText("11%", {
    x: 0.7, y: 1.3, w: 4.0, h: 1.5,
    fontSize: 100, fontFace: F, bold: true, color: C.teal, margin: 0, align: "center"
  });
  s.addText("of lapsed members responded", {
    x: 0.7, y: 2.85, w: 4.0, h: 0.4,
    fontSize: 14, fontFace: F, color: C.med, align: "center", margin: 0
  });

  // Right column: why it matters
  s.addText("Why the imbalance matters", {
    x: 5.0, y: 1.3, w: 4.3, h: 0.4,
    fontSize: 16, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  s.addText([
    { text: "Accuracy is useless: predict 'no' always = 89% accurate.\n", options: { fontSize: 12, color: C.body } },
    { text: "\n", options: {} },
    { text: "We need to maximize ", options: { fontSize: 12, color: C.body } },
    { text: "recall on the positive class", options: { fontSize: 12, color: C.body, bold: true } },
    { text: " without losing too much precision.\n", options: { fontSize: 12, color: C.body } },
    { text: "\n", options: {} },
    { text: "Two paths:\n", options: { fontSize: 12, color: C.body, bold: true } },
    { text: "  •  Resample the training data (under, over, SMOTE)\n", options: { fontSize: 11, color: C.body } },
    { text: "  •  Use class-aware models that handle imbalance internally\n", options: { fontSize: 11, color: C.body } },
  ], {
    x: 5.0, y: 1.7, w: 4.3, h: 2.7,
    fontFace: F, valign: "top", margin: 0
  });

  calloutBox(s, 0.7, 4.7, 8.6, 0.45,
    "Sampling is applied to TRAINING data only. Validation and test sets keep the original class balance — that's the population we'll deploy against.",
    "warn");
}

// ============ SLIDE 16: M3 — THE GRID ============
{
  const s = contentSlide("Module 3 — the grid");
  addTitle(s, "4 sampling × 5 algorithms = 20 combinations", "One loop function. One uniform metric table.");

  // Two-column: samplers and algorithms
  s.addText("Samplers", {
    x: 0.7, y: 1.4, w: 3.5, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  ["none  (baseline)", "RandomUnderSampler", "RandomOverSampler", "SMOTE"].forEach((it, i) => {
    s.addText(`•  ${it}`, {
      x: 0.85, y: 1.8 + i*0.32, w: 3.4, h: 0.3,
      fontSize: 12, fontFace: F, color: C.body, margin: 0
    });
  });

  s.addText("Algorithms", {
    x: 5.0, y: 1.4, w: 4.3, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  ["DecisionTreeClassifier", "LogisticRegression", "SVC (RBF kernel)", "RandomForestClassifier", "XGBClassifier"].forEach((it, i) => {
    s.addText(`•  ${it}`, {
      x: 5.15, y: 1.8 + i*0.32, w: 4.1, h: 0.3,
      fontSize: 12, fontFace: F, color: C.body, margin: 0
    });
  });

  codeBlock(s, 0.7, 3.6, 8.6, 1.4,
`for s_name, sampler in SAMPLERS.items():
    Xtr_s, ytr_s = sampler.fit_resample(Xtr, ytr) if sampler else (Xtr, ytr)
    for a_name, make_alg in ALGORITHMS.items():
        model = make_alg().fit(Xtr_s, ytr_s)
        rows.append({**evaluate(model, Xv, yv), "sampling": s_name, "algorithm": a_name})`, 11);
}

// ============ SLIDE 17: M3 — TRAIN/VAL/TEST ============
{
  const s = contentSlide("Module 3 — split");
  addTitle(s, "Train / Validation / Test  —  60 / 20 / 20", "Tune on validation. Lock the winner. Touch the test set once.");

  // Visual representation
  const totalW = 7.5;
  const segs = [
    { lbl: "Train (60%)",      w: 0.60 * totalW, color: C.teal,  use: "Fit + sample" },
    { lbl: "Validation (20%)", w: 0.20 * totalW, color: C.amber, use: "Pick winner" },
    { lbl: "Test (20%)",       w: 0.20 * totalW, color: C.green, use: "Final number" },
  ];
  let x = 1.2;
  segs.forEach((sg) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.5, w: sg.w, h: 0.7,
      fill: { color: sg.color }, line: { type: "none" }
    });
    s.addText(sg.lbl, {
      x, y: 1.5, w: sg.w, h: 0.7,
      fontSize: 13, fontFace: F, bold: true, color: C.white,
      align: "center", valign: "middle", margin: 0
    });
    s.addText(sg.use, {
      x, y: 2.25, w: sg.w, h: 0.3,
      fontSize: 10, fontFace: F, color: C.med,
      align: "center", italic: true, margin: 0
    });
    x += sg.w;
  });

  s.addText("Stratified split — each partition keeps the 11% positive rate.", {
    x: 0.7, y: 2.85, w: 8.6, h: 0.3,
    fontSize: 12, fontFace: F, color: C.body, italic: true, align: "center", margin: 0
  });

  // Metrics table
  s.addText("Metrics reported per (sampling × algorithm)", {
    x: 0.7, y: 3.4, w: 8.6, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  const metrics = [
    ["F1",        "Harmonic mean of precision and recall — the balanced view"],
    ["Precision", "Of those we flagged, how many actually responded"],
    ["Recall",    "Of those who responded, how many did we catch"],
    ["AUC",       "Ranking quality — does the model order responders above non-responders"],
  ];
  metrics.forEach((m, i) => {
    const y = 3.85 + i * 0.34;
    s.addText(m[0], {
      x: 0.7, y, w: 1.3, h: 0.3,
      fontSize: 12, fontFace: "Consolas", bold: true, color: C.teal, margin: 0
    });
    s.addText(m[1], {
      x: 2.0, y, w: 7.3, h: 0.3,
      fontSize: 11, fontFace: F, color: C.body, margin: 0
    });
  });
}

// ============ SLIDE 18: M3 — LIFT ============
{
  const s = contentSlide("Module 3 — lift");
  addTitle(s, "Lift by decile", "The chart that survives every campaign post-mortem.");

  // Sample lift table
  const headers = ["Decile", "% of pop", "Resp rate", "Lift", "Cum capture"];
  const colW = [1.4, 1.6, 1.6, 1.4, 2.5];
  const xs = [0.7, 2.1, 3.7, 5.3, 6.7];
  headers.forEach((h, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: xs[i], y: 1.4, w: colW[i], h: 0.4,
      fill: { color: C.teal }, line: { type: "none" }
    });
    s.addText(h, {
      x: xs[i], y: 1.4, w: colW[i], h: 0.4,
      fontSize: 11, fontFace: F, bold: true, color: C.white,
      align: "center", valign: "middle", margin: 0
    });
  });

  // Sample lift rows (illustrative — real numbers in the notebook)
  const lift = [
    ["1 (top)", "10%", "33%",  "3.0x", "27%"],
    ["2",       "10%", "22%",  "2.0x", "45%"],
    ["3",       "10%", "16%",  "1.5x", "59%"],
    ["4",       "10%", "12%",  "1.1x", "69%"],
    ["5",       "10%", "10%",  "0.9x", "78%"],
    ["6-10",    "50%", "5%",   "0.5x", "100%"],
  ];
  lift.forEach((r, i) => {
    const y = 1.8 + i * 0.32;
    const fill = i % 2 === 0 ? C.white : C.card;
    r.forEach((cell, j) => {
      s.addShape(pres.shapes.RECTANGLE, {
        x: xs[j], y, w: colW[j], h: 0.32,
        fill: { color: fill }, line: { color: C.divider, width: 0.5 }
      });
      const isLift = j === 3;
      s.addText(cell, {
        x: xs[j] + 0.05, y, w: colW[j] - 0.1, h: 0.32,
        fontSize: 11, fontFace: isLift ? "Consolas" : F,
        color: isLift ? C.teal : C.body,
        bold: isLift,
        align: j === 0 ? "left" : "center",
        valign: "middle", margin: 0
      });
    });
  });

  calloutBox(s, 0.7, 4.0, 8.6, 0.95,
    "Read it like a campaign manager: 'If we send to the top 30% (3 deciles), we capture 59% of all responders at ~2x the base rate.' That's the answer to 'who do we target?' — not 'which model has higher AUC.'",
    "tip");
}

// ============ SLIDE 19: M4 DIVIDER ============
dividerSlide("04", "Segment", "How many real types of customer do we have?");

// ============ SLIDE 20: M4 — SINGLE VIEW ============
{
  const s = contentSlide("Module 4 — single view");
  addTitle(s, "Customer Single View", "One row per customer. Every behavior collapsed.");

  // 3 columns of features
  const cols = [
    { title: "RFM core", items: ["recency (days)", "frequency (visits)", "monetary (baht)", "avg_ticket"] },
    { title: "Channel mix", items: ["app_share", "delivery_share", "dinein_share", "weekend_share"] },
    { title: "Behavior depth", items: ["promo_share", "avg_basket_size", "tenure_days", "active_span"] },
  ];

  cols.forEach((col, i) => {
    const x = 0.7 + i * 2.95;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.4, w: 2.7, h: 2.6,
      fill: { color: C.card }, line: { color: C.divider, width: 0.5 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y: 1.4, w: 2.7, h: 0.07,
      fill: { color: C.teal }, line: { type: "none" }
    });
    s.addText(col.title, {
      x: x + 0.15, y: 1.55, w: 2.4, h: 0.35,
      fontSize: 14, fontFace: F, bold: true, color: C.dark, margin: 0
    });
    col.items.forEach((it, j) => {
      s.addText(`•  ${it}`, {
        x: x + 0.2, y: 1.95 + j * 0.32, w: 2.35, h: 0.3,
        fontSize: 11, fontFace: "Consolas", color: C.body, margin: 0
      });
    });
  });

  calloutBox(s, 0.7, 4.2, 8.6, 0.85,
    "The single view is the unsung hero of analytics. It is what you build once and reuse for segmentation, churn, LTV, and recommendation. Most data debt at retail clients is the absence of this table.",
    "tip");
}

// ============ SLIDE 21: M4 — CLUSTERS ============
{
  const s = contentSlide("Module 4 — clusters");
  addTitle(s, "K-means + silhouette", "Pick k by data, not by gut. Then name the clusters from their profiles.");

  // 4 segment cards
  const segs = [
    { name: "Daily Loyalists",   color: C.teal,   stats: "freq ~ 149  •  recency ~ 7d  •  monetary ~ 18K" },
    { name: "Weekend Brunchers", color: C.amber,  stats: "freq ~ 45   •  weekend_share > 45%  •  bigger ticket" },
    { name: "App Promo Hunters", color: C.purple, stats: "freq ~ 59   •  app_share > 50%  •  promo_share elevated" },
    { name: "Casual Drifters",   color: C.red,    stats: "freq ~ 16   •  recency ~ 66d  •  ~half lapse out" },
  ];

  segs.forEach((sg, i) => {
    const row = Math.floor(i / 2);
    const col = i % 2;
    const x = 0.7 + col * 4.4;
    const y = 1.4 + row * 1.45;
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 4.1, h: 1.25,
      fill: { color: C.card }, line: { color: C.divider, width: 0.5 }
    });
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w: 0.08, h: 1.25, fill: { color: sg.color }, line: { type: "none" }
    });
    s.addText(sg.name, {
      x: x + 0.2, y: y + 0.1, w: 3.8, h: 0.35,
      fontSize: 16, fontFace: F, bold: true, color: C.dark, margin: 0
    });
    s.addText(sg.stats, {
      x: x + 0.2, y: y + 0.5, w: 3.8, h: 0.6,
      fontSize: 11, fontFace: "Consolas", color: C.body, margin: 0
    });
  });

  calloutBox(s, 0.7, 4.4, 8.6, 0.55,
    "The cross-tab against the engineered ground-truth labels validates the clusters. In real client work you don't have ground truth — that's why you stress-test cluster stability with multiple k and seeds.",
    "tip");
}

// ============ SLIDE 22: M4 — RECOMMENDATION ============
{
  const s = contentSlide("Module 4 — recommendation");
  addTitle(s, "Item-item recommendation + segment network", "Co-purchase similarity → segment ↔ top-product graph");

  // Two columns
  s.addText("Item-item cosine similarity", {
    x: 0.7, y: 1.4, w: 4.1, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  codeBlock(s, 0.7, 1.8, 4.1, 1.6,
`matrix = cp.pivot(
  index='customer_id',
  columns='product_id',
  values='n').fillna(0)
sim = cosine_similarity(
  (matrix>0).astype(int).T)`, 10);
  s.addText("→ Latte → top neighbors: Croissant, Espresso, Almond Croissant, Cinnamon Roll, Brownie", {
    x: 0.7, y: 3.45, w: 4.1, h: 0.6,
    fontSize: 11, fontFace: F, color: C.body, italic: true, margin: 0, valign: "top"
  });

  s.addText("Segment ↔ top product network", {
    x: 5.0, y: 1.4, w: 4.3, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  s.addText([
    { text: "Nodes: ", options: { fontSize: 12, color: C.body, bold: true } },
    { text: "segments (teal) + products (amber)\n", options: { fontSize: 12, color: C.body } },
    { text: "Edges: ", options: { fontSize: 12, color: C.body, bold: true } },
    { text: "weighted by purchase volume per segment\n", options: { fontSize: 12, color: C.body } },
    { text: "Look for: ", options: { fontSize: 12, color: C.body, bold: true } },
    { text: "products that bridge multiple segments — those are your anchor SKUs for cross-segment campaigns.", options: { fontSize: 12, color: C.body } },
  ], {
    x: 5.0, y: 1.8, w: 4.3, h: 2.5,
    fontFace: F, valign: "top", margin: 0
  });

  calloutBox(s, 0.7, 4.4, 8.6, 0.55,
    "The graph is not just a pretty picture. Bridge products are operationally important — they're what you put on the loyalty home screen for everyone.",
    "tip");
}

// ============ SLIDE 23: M5 DIVIDER ============
dividerSlide("05", "Listen", "What are customers actually saying?");

// ============ SLIDE 24: M5 — PYTHAINLP ============
{
  const s = contentSlide("Module 5 — PyThaiNLP");
  addTitle(s, "Tokenize Thai. Clean. POS-tag.", "PyThaiNLP gets you 80% of the way for Thai text analytics.");

  codeBlock(s, 0.7, 1.4, 8.6, 2.4,
`from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from pythainlp.tag import pos_tag

THAI_STOPS = set(thai_stopwords())

def tokenize_thai_en(text):
    tokens = word_tokenize(text, engine='newmm')
    return [t for t in tokens if t not in THAI_STOPS
            and not re.fullmatch(r'[\\d\\W_]+', t)]

# Example: "ร้านดีมาก กาแฟอร่อย พนักงานบริการดี"
# →  ['ร้าน', 'ดีมาก', 'กาแฟ', 'อร่อย', 'พนักงาน', 'บริการ', 'ดี']`, 11);

  calloutBox(s, 0.7, 3.95, 8.6, 1.05,
    "Thai has no spaces between words, mixed-script reviews are normal, and English code-switches in mid-sentence ('wifi ช้ามาก'). PyThaiNLP's newmm tokenizer handles this gracefully. NER requires a corpus download — POS-based extraction is the dependable fallback.",
    "tip");
}

// ============ SLIDE 25: M5 — BIGRAM NETWORK ============
{
  const s = contentSlide("Module 5 — bi-grams");
  addTitle(s, "Bi-gram network", "What words travel together → the latent topics emerge");

  s.addText([
    { text: "1.  ", options: { color: C.teal, bold: true, fontSize: 13 } },
    { text: "Tokenize each review, filter stopwords\n", options: { fontSize: 13, color: C.body } },
    { text: "2.  ", options: { color: C.teal, bold: true, fontSize: 13 } },
    { text: "Build all (word_i, word_i+1) pairs\n", options: { fontSize: 13, color: C.body } },
    { text: "3.  ", options: { color: C.teal, bold: true, fontSize: 13 } },
    { text: "Count across the corpus, keep pairs with count ≥ 8\n", options: { fontSize: 13, color: C.body } },
    { text: "4.  ", options: { color: C.teal, bold: true, fontSize: 13 } },
    { text: "Build NetworkX graph — nodes = words, edges = bi-gram pairs, edge weight = count\n", options: { fontSize: 13, color: C.body } },
    { text: "5.  ", options: { color: C.teal, bold: true, fontSize: 13 } },
    { text: "Force-directed layout (spring) → semantic clusters appear as dense subgraphs\n", options: { fontSize: 13, color: C.body } },
  ], {
    x: 0.7, y: 1.4, w: 8.6, h: 2.5,
    fontFace: F, valign: "top", margin: 0
  });

  calloutBox(s, 0.7, 4.0, 8.6, 1.0,
    "The bi-gram net is the cheapest topic model. You'll see a 'wait time' cluster (รอ-นาน-คิว-ยาว), a 'taste' cluster (อร่อย-กาแฟ-หอม), and a 'service' cluster (พนักงาน-บริการ-ดี). No model fitting required.",
    "tip");
}

// ============ SLIDE 26: M5 — ENTITY-ADJ NETWORK ============
{
  const s = contentSlide("Module 5 — entities");
  addTitle(s, "Entity ↔ adjective network", "Nouns are what they talk about. Adjectives are what they call it.");

  // POS table
  s.addText("POS tags we use (ORCHID tagset)", {
    x: 0.7, y: 1.4, w: 8.6, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.dark, margin: 0
  });
  const tags = [
    ["NCMN, NPRP, NTTL", "common nouns, proper nouns, titles", "→ entities", C.teal],
    ["VATT, ADJX, ADVN", "stative-attributive verbs, adjectives", "→ descriptors", C.amber],
  ];
  tags.forEach((row, i) => {
    const y = 1.85 + i * 0.5;
    s.addText(row[0], {
      x: 0.7, y, w: 2.5, h: 0.4,
      fontSize: 13, fontFace: "Consolas", color: row[3], bold: true, margin: 0
    });
    s.addText(row[1], {
      x: 3.3, y, w: 4.0, h: 0.4,
      fontSize: 12, fontFace: F, color: C.body, margin: 0
    });
    s.addText(row[2], {
      x: 7.4, y, w: 1.9, h: 0.4,
      fontSize: 12, fontFace: F, color: row[3], italic: true, bold: true, margin: 0
    });
  });

  s.addText("Co-occurrence within the same review → edge in the entity-adjective graph", {
    x: 0.7, y: 3.0, w: 8.6, h: 0.3,
    fontSize: 12, fontFace: F, color: C.body, italic: true, margin: 0
  });

  codeBlock(s, 0.7, 3.4, 8.6, 1.6,
`for review in reviews:
    nouns = [w for w, t in pos_tag(tokens) if t in {'NCMN','NPRP','NTTL'}]
    adjs  = [w for w, t in pos_tag(tokens) if t in {'VATT','ADJX','ADVN'}]
    for n in nouns:
        for a in adjs:
            pairs[(n, a)] += 1`, 11);
}

// ============ SLIDE 27: M5 — THONGLOR REVEAL ============
{
  const s = contentSlide("Module 5 — leading indicator");
  addTitle(s, "The Thonglor reveal", "Numbers say everything's fine. Reviews say it isn't.");

  // Two-column comparison
  s.addText("Last 6 weeks", {
    x: 0.7, y: 1.4, w: 4.1, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.red, margin: 0
  });
  s.addText("63% negative reviews", {
    x: 0.7, y: 1.8, w: 4.1, h: 0.5,
    fontSize: 26, fontFace: F, bold: true, color: C.red, margin: 0
  });
  s.addText("Avg rating: 3.7  (only -0.4 vs prior)", {
    x: 0.7, y: 2.4, w: 4.1, h: 0.35,
    fontSize: 12, fontFace: F, color: C.body, italic: true, margin: 0
  });

  s.addText("Prior period", {
    x: 5.0, y: 1.4, w: 4.3, h: 0.35,
    fontSize: 14, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  s.addText("23% negative reviews", {
    x: 5.0, y: 1.8, w: 4.3, h: 0.5,
    fontSize: 26, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  s.addText("Avg rating: 4.1", {
    x: 5.0, y: 2.4, w: 4.3, h: 0.35,
    fontSize: 12, fontFace: F, color: C.body, italic: true, margin: 0
  });

  // The takeaway
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 3.0, w: 8.6, h: 1.45,
    fill: { color: C.amber_bg }, line: { color: C.amber, width: 1 }
  });
  s.addText("The leading indicator", {
    x: 0.85, y: 3.1, w: 8.4, h: 0.35,
    fontSize: 16, fontFace: F, bold: true, color: C.amber, margin: 0
  });
  s.addText("Negative review volume tripled. Average rating barely moved. By the time the rating drops, the customers are already gone — they're rating their last visit, not their next.\n\nThis is what dashboards miss. Sentiment monitoring catches it weeks earlier.", {
    x: 0.85, y: 3.45, w: 8.4, h: 0.95,
    fontSize: 12, fontFace: F, color: C.body, valign: "top", margin: 0
  });

  calloutBox(s, 0.7, 4.6, 8.6, 0.5,
    "The Thonglor pattern is engineered into the data. But it is exactly the kind of pattern you find at every Thai retail client when you actually read the reviews.",
    "warn");
}

// ============ SLIDE 28: CLOSING — THE LOOP ============
{
  const s = contentSlide("Closing");
  addTitle(s, "The loop closes", "Five modules. One thread. The techniques compose.");

  // Diagram-like flow
  s.addText("[Module 1] What's true", {
    x: 0.7, y: 1.5, w: 2.7, h: 0.4,
    fontSize: 13, fontFace: F, bold: true, color: C.teal, margin: 0
  });
  s.addText("[Module 2] What's coming", {
    x: 3.65, y: 1.5, w: 2.7, h: 0.4,
    fontSize: 13, fontFace: F, bold: true, color: C.green, margin: 0
  });
  s.addText("[Module 5] What they say", {
    x: 6.6, y: 1.5, w: 2.7, h: 0.4,
    fontSize: 13, fontFace: F, bold: true, color: C.red, margin: 0
  });

  s.addText("↓", {
    x: 6.6, y: 1.95, w: 2.7, h: 0.4,
    fontSize: 18, fontFace: F, color: C.red, margin: 0
  });
  s.addText("sentiment as feature", {
    x: 6.6, y: 2.3, w: 2.7, h: 0.3,
    fontSize: 10, fontFace: F, color: C.med, italic: true, margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 3.0, y: 2.8, w: 4.0, h: 0.6,
    fill: { color: C.amber }, line: { type: "none" }
  });
  s.addText("[Module 3] Who responds", {
    x: 3.0, y: 2.8, w: 4.0, h: 0.6,
    fontSize: 14, fontFace: F, bold: true, color: C.white,
    align: "center", valign: "middle", margin: 0
  });

  s.addText("↓ segment as filter", {
    x: 3.0, y: 3.5, w: 4.0, h: 0.3,
    fontSize: 11, fontFace: F, color: C.med,
    align: "center", italic: true, margin: 0
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 3.0, y: 3.9, w: 4.0, h: 0.6,
    fill: { color: C.purple }, line: { type: "none" }
  });
  s.addText("[Module 4] Who they are", {
    x: 3.0, y: 3.9, w: 4.0, h: 0.6,
    fontSize: 14, fontFace: F, bold: true, color: C.white,
    align: "center", valign: "middle", margin: 0
  });

  calloutBox(s, 0.7, 4.7, 8.6, 0.5,
    "Module 5's sentiment becomes a feature in Module 3. Module 4's segments filter Module 3's targets. Module 1's findings calibrate Module 2's forecasts. The techniques are not silos.",
    "tip");
}

// ============ SLIDE 29: WHAT YOU TAKE AWAY ============
{
  const s = contentSlide("Takeaways");
  addTitle(s, "Eight habits worth taking with you", "If you remember nothing else.");

  const habits = [
    "1. Pre-register hypotheses. The dictionary is the audit trail.",
    "2. Pick the test by data type — not by what you remember.",
    "3. FDR-correct when you sweep. Always.",
    "4. Confirm with regression + interactions when the simple test surprises you.",
    "5. Try the simple forecasts first. They often win.",
    "6. Measure model fit with the metric the business actually cares about.",
    "7. Imbalanced classes need stratified splits and lift charts. Accuracy is misleading.",
    "8. Read the reviews. Sentiment is a leading indicator for the dashboards.",
  ];
  habits.forEach((h, i) => {
    const y = 1.4 + i * 0.42;
    s.addText(h, {
      x: 0.7, y, w: 8.6, h: 0.4,
      fontSize: 13, fontFace: F, color: C.body, margin: 0
    });
  });

  calloutBox(s, 0.7, 4.85, 8.6, 0.4,
    "These habits travel. Different industry, different tools — same disciplines.",
    "tip");
}

// ============ SLIDE 30: CLOSING ============
{
  const s = pres.addSlide();
  s.background = { color: C.dark };
  addTopBar(s);
  s.addText("MADT", {
    x: 8.4, y: 0.25, w: 1.2, h: 0.4,
    fontSize: 13, fontFace: F, bold: true, color: C.teal, align: "right"
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 1.85, w: 0.08, h: 1.5,
    fill: { color: C.teal }, line: { type: "none" }
  });
  s.addText("Thank you.", {
    x: 0.95, y: 1.8, w: 8.4, h: 0.9,
    fontSize: 44, fontFace: F, bold: true, color: C.white, margin: 0
  });
  s.addText("Now build something with it.", {
    x: 0.95, y: 2.7, w: 8.4, h: 0.5,
    fontSize: 18, fontFace: F, color: C.light, italic: true, margin: 0
  });

  s.addText("github.com/thanachart/MADT6004  →  Integrated Data Analytics Exercise", {
    x: 0.7, y: 4.5, w: 8.6, h: 0.3,
    fontSize: 12, fontFace: "Consolas", color: C.teal, margin: 0
  });
  s.addText("MADT6004  |  Asst. Prof. Dr. Thanachart Ritbumroong  |  NIDA", {
    x: 0.7, y: 4.85, w: 8.6, h: 0.3,
    fontSize: 12, fontFace: F, color: C.light, margin: 0
  });
}

// Save
pres.writeFile({ fileName: "MADT6004_Wrap_Up_Session.pptx" }).then((file) => {
  console.log("Wrote:", file);
});
