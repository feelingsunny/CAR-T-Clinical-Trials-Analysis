# CAR-T Clinical Trials Analysis Pipeline

An end-to-end data analysis pipeline examining **2,913 real-world CAR-T (Chimeric Antigen Receptor T-cell) clinical trials** from ClinicalTrials.gov, combining SQL database design, Python data engineering, and Power BI visualization.

---

## Project Background

CAR-T therapy is one of the fastest-growing areas in oncology, with trial volume growing dramatically since 2015. This project analyzes global CAR-T trial trends across cancer types, trial phases, geographic distribution, and leading treatment products — combining biomedical domain expertise with data engineering and analysis skills.

**Key findings from the data:**
- CAR-T trial volume grew 20x between 2010 and 2025
- China leads globally with ~1,900 trials, followed by the US (~1,000)
- Phase 1 trials dominate (1,125 trials), reflecting the field's early-stage nature
- 35% of trials are actively recruiting, showing continued rapid expansion
- Phase 3 trials have the highest average enrollment (~320 patients per trial)

---

## Tech Stack

| Layer | Tools |
|---|---|
| Database | PostgreSQL |
| SQL | Joins, aggregations, window functions, ETL |
| Data pipeline | Python, Pandas, Requests, SQLAlchemy |
| Visualization | Power BI Desktop |
| Version control | Git / GitHub |

---

## Project Structure

```
CAR-T-Clinical-Trials-Analysis/
├── data/
│   ├── cart_trials_raw.json        # Raw API response (2,913 records)
│   └── cart_trials_clean.csv       # Cleaned, flattened dataset
├── sql/
│   └── queries.sql                 # 6 analysis queries
├── python/
│   ├── fetch_cart_data.py          # Pull data from ClinicalTrials.gov API
│   ├── generate_mock_data.py       # Mock data generator for local dev
│   └── fix_phase_labels.py         # Phase label standardization
├── dashboard/
│   └── cart_trials_dashboard.pbix  # Power BI dashboard (4 visualizations)
└── README.md
```

---

## Database Schema

5 normalized tables with foreign key relationships:

```
trials          — core trial information (status, phase, enrollment, sponsor)
conditions      — cancer types per trial (one-to-many)
interventions   — CAR-T products per trial (one-to-many)
locations       — countries per trial (one-to-many)
eligibility     — patient criteria (age, gender, pediatric flag)
```

---

## SQL Analysis Queries

| Query | Technique | Key Finding |
|---|---|---|
| Trial growth by year | GROUP BY, aggregation | 20x growth from 2010 to 2025 |
| Trials by cancer type | JOIN, AVG | B-cell malignancies most studied |
| Completion rate by phase | CASE WHEN, percentage | Phase 3 completion rate lowest |
| Geographic distribution | JOIN, COUNT | China #1, US #2 |
| CAR-T product analysis | JOIN, ORDER BY | Multiple FDA-approved products |
| Pediatric vs adult | Window function, PARTITION BY | Phase 3 has highest enrollment |

---

## Power BI Dashboard

4 interactive visualizations:

1. **CAR-T Trial Growth by Year** — line chart showing explosive growth post-2015
2. **Trials by Country** — bar chart highlighting China/US dominance
3. **Trial Status Distribution** — pie chart showing 35% actively recruiting
4. **Average Enrollment by Phase** — bar chart comparing Phase 1 through 4

---

## How to Run

### Fetch real data
```bash
pip install requests pandas
python python/fetch_cart_data.py
```

### Fix phase labels
```bash
python python/fix_phase_labels.py
```

### Set up PostgreSQL database
```sql
-- Run in psql:
CREATE DATABASE cart_trials;
\c cart_trials
-- Then paste contents of sql/queries.sql
```

---

## Data Source

[ClinicalTrials.gov](https://clinicaltrials.gov) — U.S. National Library of Medicine  
API: https://clinicaltrials.gov/data-api/api  
Data retrieved: August 2026

---

## Author

**Yang Liu**  
Research Associate, University of Manitoba  
[LinkedIn](https://www.linkedin.com/in/yang-liu-6093/) | [GitHub](https://github.com/feelingsunny)
