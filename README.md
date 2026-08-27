# CAR-T Clinical Trials & Treatment Analysis Pipeline

[![Monthly Data Update](https://github.com/feelingsunny/CAR-T-Clinical-Trials-Analysis/actions/workflows/monthly_update.yml/badge.svg)](https://github.com/feelingsunny/CAR-T-Clinical-Trials-Analysis/actions/workflows/monthly_update.yml)
[![Deploy to Pages](https://github.com/feelingsunny/CAR-T-Clinical-Trials-Analysis/actions/workflows/static.yml/badge.svg)](https://github.com/feelingsunny/CAR-T-Clinical-Trials-Analysis/actions/workflows/static.yml)

An end-to-end data pipeline analyzing **2,913 real-world CAR-T clinical trials** and **global treatment availability** across 7 countries — combining SQL database design, Python data engineering, Power BI visualization, and interactive web publishing.

---

## 🌐 Live Websites

| Site | URL |
|---|---|
| 📊 Data Analysis | [feelingsunny.github.io/CAR-T-Clinical-Trials-Analysis](https://feelingsunny.github.io/CAR-T-Clinical-Trials-Analysis/) |
| 💼 Investor Presentation | [feelingsunny.github.io/CAR-T-Clinical-Trials-Analysis/investor.html](https://feelingsunny.github.io/CAR-T-Clinical-Trials-Analysis/investor.html) |

---

## 🔄 Automated Monthly Updates

This repository uses **GitHub Actions** to automatically refresh all data on the 1st of every month:

- Fetches latest CAR-T trials from ClinicalTrials.gov API
- Standardizes phase labels and cleans data
- Updates treatment cost and product comparison data
- Commits and pushes updated CSV files to the repository
- GitHub Pages website updates automatically

**No manual intervention required.**

---

## Key Findings

### Clinical Trials (2,913 records · August 2026)
- CAR-T trial volume grew **20×** between 2010 and 2025
- China leads globally with **~1,900 trials**, followed by the US (~1,000)
- Phase 1 trials dominate (1,125), reflecting the field's early-stage nature
- 35% of trials are actively recruiting — field still in rapid expansion

### Global Treatment Comparison (July 2026)
- China has **9 NMPA-approved products** — more than any other country
- China total all-in cost: **$50,000–$80,000** vs USA $488,000–$760,000
- China average wait time: **2–3 weeks** vs USA 12 weeks, Canada 18 weeks
- 🚨 **World first**: China approved Satri-cel (June 22, 2026) — first CAR-T for solid tumors (gastric cancer), not yet available anywhere else

---

## Tech Stack

| Layer | Tools |
|---|---|
| Database | PostgreSQL |
| SQL | Joins, aggregations, window functions, ETL |
| Data pipeline | Python, Pandas, Requests |
| Visualization | Power BI Desktop |
| Web | HTML, CSS, Chart.js (interactive, bilingual) |
| Automation | GitHub Actions (monthly cron) |
| Version control | Git / GitHub |

---

## Project Structure

```
CAR-T-Clinical-Trials-Analysis/
├── .github/
│   └── workflows/
│       ├── static.yml              # GitHub Pages auto-deploy
│       └── monthly_update.yml      # Monthly data refresh (1st of each month)
├── data/
│   ├── cart_trials_raw.json        # Raw API response (2,913 records)
│   ├── cart_trials_clean.csv       # Cleaned trials dataset (auto-updated)
│   ├── approved_products.csv       # FDA & NMPA approved products (2026)
│   ├── cost_comparison.csv         # Treatment costs by country (2026)
│   └── treatment_centers.csv       # Top CAR-T hospitals worldwide
├── sql/
│   └── queries.sql                 # 6 analysis queries
├── python/
│   ├── fetch_cart_data.py          # Pull data from ClinicalTrials.gov API
│   ├── generate_mock_data.py       # Mock data generator for local dev
│   ├── fix_phase_labels.py         # Phase label standardization
│   ├── collect_treatment_data.py   # Treatment comparison data
│   └── update_treatment_data_2026.py  # Latest 2026 data update
├── dashboard/
│   └── cart_trials_dashboard.pbix  # Power BI dashboard (2 pages)
├── index.html                      # Data analysis website
├── investor.html                   # Investor presentation website (bilingual)
└── README.md
```

---

## Dashboard Pages

### Page 1 — Clinical Trials Analysis
| Chart | Type | Key Insight |
|---|---|---|
| CAR-T Trial Growth by Year | Line chart | 20× growth 2010–2025 |
| Trials by Country | Bar chart | China #1, USA #2 |
| Trial Status Distribution | Pie chart | 35% actively recruiting |
| Average Enrollment by Phase | Bar chart | Phase 3 highest enrollment (~320 patients) |

### Page 2 — Global Treatment Comparison
| Chart | Type | Key Insight |
|---|---|---|
| Total Cost by Country | Bar chart | USA $600K vs China $90K |
| Wait Time by Country | Bar chart | Canada 18 wks vs China 3 wks |
| Approved Products by Country | Bar chart | China leads with 9 products |
| Top Treatment Centers | Table | 10 hospitals with costs and wait times |

---

## SQL Analysis Queries

| Query | Technique | Key Finding |
|---|---|---|
| Trial growth by year | GROUP BY, aggregation | 20× growth 2010–2025 |
| Trials by cancer type | JOIN, AVG | B-cell malignancies most studied |
| Completion rate by phase | CASE WHEN, percentage | Phase 2 highest completion rate |
| Geographic distribution | JOIN, COUNT | China #1, US #2 |
| CAR-T product analysis | JOIN, ORDER BY | 14 major products analyzed |
| Pediatric vs adult | Window function, PARTITION BY | Phase 3 highest enrollment |

---

## How to Run Locally

### Fetch real data
```bash
pip install requests pandas
python python/fetch_cart_data.py
python python/fix_phase_labels.py
```

### Update treatment comparison data
```bash
python python/update_treatment_data_2026.py
```

### Set up PostgreSQL database
```sql
CREATE DATABASE cart_trials;
\c cart_trials
-- paste contents of sql/queries.sql
```

### Run monthly update manually
Go to **Actions** → **Monthly CAR-T Data Update** → **Run workflow**

---

## Data Sources

- **Clinical Trials**: [ClinicalTrials.gov](https://clinicaltrials.gov) API v2 — auto-updated monthly
- **FDA Approvals**: U.S. Food & Drug Administration
- **NMPA Approvals**: China National Medical Products Administration
- **Treatment Costs**: Published medical literature and hospital websites (2026)
- **Satri-cel approval**: CARsgen press release, June 22, 2026

---

## Business Application

This analysis underpins **CARTBridge Health** — a cross-border CAR-T medical coordination service connecting North American cancer patients with top treatment centers in China, and Chinese patients seeking FDA-approved products in North America.

🌐 [View Investor Presentation](https://feelingsunny.github.io/CAR-T-Clinical-Trials-Analysis/investor.html)

---

## Author

**Yang Liu**
Research Associate, University of Manitoba
Biomedical researcher with expertise in microfluidics, point-of-care diagnostics, and data analysis

[LinkedIn](https://www.linkedin.com/in/yang-liu-6093/) · [GitHub](https://github.com/feelingsunny) · liuyang6093@gmail.com
