# CAR-T Clinical Trials & Treatment Analysis Pipeline

An end-to-end data analysis pipeline examining **2,913 real-world CAR-T (Chimeric Antigen Receptor T-cell) clinical trials** and **global treatment availability** across 7 countries, combining SQL database design, Python data engineering, and Power BI visualization.

---

## Project Background

CAR-T therapy is one of the fastest-growing areas in oncology. This project has two modules:

**Module 1 — Clinical Trials Analysis**
Analyzes global CAR-T trial trends across cancer types, trial phases, and geographic distribution using data from ClinicalTrials.gov.

**Module 2 — Global Treatment Comparison**
Compares CAR-T treatment availability, cost, wait times, and approved products across USA, China, Canada, Germany, UK, Japan, and India — answering the question: *Why are cancer patients flying to China for CAR-T treatment?*

---

## Key Findings

### Clinical Trials (2,913 records)
- CAR-T trial volume grew **20x** between 2010 and 2025
- China leads globally with **~1,900 trials**, followed by the US (~1,000)
- Phase 1 trials dominate (1,125 trials), reflecting the field's early-stage nature
- 35% of trials are actively recruiting, showing continued rapid expansion

### Global Treatment Comparison (July 2026)
- China has **9 NMPA-approved products** — more than any other country
- China total treatment cost: **$50,000–$80,000** vs USA $488,000–$760,000
- China average wait time: **2–3 weeks** vs USA 12 weeks, Canada 18 weeks
- 🚨 **World first**: China approved Satri-cel (June 22, 2026) — the first CAR-T therapy for solid tumors (gastric cancer), not yet available anywhere else

---

## Tech Stack

| Layer | Tools |
|---|---|
| Database | PostgreSQL |
| SQL | Joins, aggregations, window functions, ETL |
| Data pipeline | Python, Pandas, Requests |
| Visualization | Power BI Desktop |
| Version control | Git / GitHub |

---

## Project Structure

```
CAR-T-Clinical-Trials-Analysis/
├── data/
│   ├── cart_trials_raw.json           # Raw API response (2,913 records)
│   ├── cart_trials_clean.csv          # Cleaned trials dataset
│   ├── approved_products.csv          # FDA & NMPA approved products (2026)
│   ├── cost_comparison.csv            # Treatment costs by country (2026)
│   └── treatment_centers.csv          # Top CAR-T hospitals worldwide
├── sql/
│   └── queries.sql                    # 6 analysis queries
├── python/
│   ├── fetch_cart_data.py             # Pull data from ClinicalTrials.gov API
│   ├── generate_mock_data.py          # Mock data generator
│   ├── fix_phase_labels.py            # Phase label standardization
│   ├── collect_treatment_data.py      # Treatment comparison data
│   └── update_treatment_data_2026.py  # Latest 2026 data update
├── dashboard/
│   └── cart_trials_dashboard.pbix     # Power BI (2 pages)
└── README.md
```

---

## Dashboard Pages

### Page 1 — Clinical Trials Analysis
| Chart | Type | Key Insight |
|---|---|---|
| CAR-T Trial Growth by Year | Line chart | 20x growth 2010–2025 |
| Trials by Country | Bar chart | China #1, USA #2 |
| Trial Status Distribution | Pie chart | 35% actively recruiting |
| Average Enrollment by Phase | Bar chart | Phase 3 highest enrollment |

### Page 2 — Global Treatment Comparison
| Chart | Type | Key Insight |
|---|---|---|
| Total Cost by Country | Bar chart | USA $600K vs China $90K |
| Wait Time by Country | Bar chart | Canada 18wks vs China 3wks |
| Approved Products by Country | Bar chart | China leads with 9 products |
| Top Treatment Centers | Table | 10 hospitals, costs, wait times |

---

## Database Schema

5 normalized PostgreSQL tables:

```
trials          — core trial info (status, phase, enrollment, sponsor)
conditions      — cancer types per trial (one-to-many)
interventions   — CAR-T products per trial (one-to-many)
locations       — countries per trial (one-to-many)
eligibility     — patient criteria (age, gender, pediatric flag)
```

---

## SQL Analysis Queries

| Query | Technique | Key Finding |
|---|---|---|
| Trial growth by year | GROUP BY, aggregation | 20x growth 2010–2025 |
| Trials by cancer type | JOIN, AVG | B-cell malignancies most studied |
| Completion rate by phase | CASE WHEN, percentage | Phase 2 highest completion rate |
| Geographic distribution | JOIN, COUNT | China #1, US #2 |
| CAR-T product analysis | JOIN, ORDER BY | 14 major products analyzed |
| Pediatric vs adult | Window function, PARTITION BY | Phase 3 highest enrollment |

---

## How to Run

### Fetch real clinical trials data
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

---

## Data Sources

- **Clinical Trials**: [ClinicalTrials.gov](https://clinicaltrials.gov) API v2 — retrieved August 2026
- **FDA Approvals**: U.S. Food & Drug Administration
- **NMPA Approvals**: China National Medical Products Administration
- **Treatment Costs**: Published medical literature and hospital websites (2026)
- **Satri-cel approval**: CARsgen press release, June 22, 2026

---

## Author

**Yang Liu**
Research Associate, University of Manitoba
Biomedical researcher with expertise in microfluidics, point-of-care diagnostics, and data analysis

[LinkedIn](https://www.linkedin.com/in/yang-liu-6093/) | [GitHub](https://github.com/feelingsunny)
